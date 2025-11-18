

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define MAX_DRAWS   20000
#define NUM_BALLS   6
#define NUM_DEZENAS 60

typedef struct {
    int n;                        
    unsigned char y[NUM_DEZENAS][MAX_DRAWS]; 
} Indicator;

static int cmp_desc_pair(const void *a, const void *b) {
    const double *pa = (const double *)a;
    const double *pb = (const double *)b;
    if (pb[0] > pa[0]) return 1;
    if (pb[0] < pa[0]) return -1;
    return 0;
}

static int read_csv(const char *path, int draws[MAX_DRAWS][NUM_BALLS]) {
    FILE *f = fopen(path, "r");
    if (!f) { perror("fopen"); return -1; }
    char line[4096];
    int n = 0;

    while (fgets(line, sizeof(line), f)) {
        // troca separadores por espaço
        for (char *p = line; *p; ++p) {
            if (*p == ',' || *p == ';' || *p == '\t' || *p == '\r' || *p == '\n')
                *p = ' ';
        }
        // extração dos 6 primeiros inteiros válidos
        int v[NUM_BALLS], cnt = 0;
        char *tok = strtok(line, " ");
        while (tok && cnt < NUM_BALLS) {
            char *end = NULL;
            long x = strtol(tok, &end, 10);
            if (end != tok && x >= 1 && x <= 60) {
                v[cnt++] = (int)x;
            }
            tok = strtok(NULL, " ");
        }
        if (cnt == NUM_BALLS) {
            for (int j = 0; j < NUM_BALLS; ++j) draws[n][j] = v[j];
            n++;
            if (n >= MAX_DRAWS) break;
        }
    }
    fclose(f);
    return n;
}

static void build_indicator(const int draws[MAX_DRAWS][NUM_BALLS], int n, Indicator *ind) {
    ind->n = n;
    for (int d = 0; d < NUM_DEZENAS; ++d)
        for (int t = 0; t < n; ++t) ind->y[d][t] = 0;

    for (int t = 0; t < n; ++t) {
        for (int k = 0; k < NUM_BALLS; ++k) {
            int v = draws[t][k];
            if (1 <= v && v <= NUM_DEZENAS) ind->y[v-1][t] = 1;
        }
    }
}

static void freq_historica(const Indicator *ind, double out[NUM_DEZENAS]) {
    int n = ind->n;
    for (int d = 0; d < NUM_DEZENAS; ++d) {
        int s = 0;
        for (int t = 0; t < n; ++t) s += ind->y[d][t];
        out[d] = (double)s / (double)n;
    }
}

static void media_movel_last(const Indicator *ind, int W, double out[NUM_DEZENAS]) {
    int n = ind->n;
    if (W < 1) W = 1;
    if (W > n) W = n;
    int start = n - W;
    for (int d = 0; d < NUM_DEZENAS; ++d) {
        int s = 0;
        for (int t = start; t < n; ++t) s += ind->y[d][t];
        out[d] = (double)s / (double)W;
    }
}


static void ar1_forecast(const Indicator *ind, double out[NUM_DEZENAS]) {
    int n = ind->n;
    for (int d = 0; d < NUM_DEZENAS; ++d) {
        const unsigned char *y = ind->y[d];
        if (n < 3) { out[d] = (double)y[n-1]; continue; }

        double sum_y = 0, sum_lag = 0, sum_lag2 = 0, sum_y_lag = 0;
        for (int t = 1; t < n; ++t) {
            double yt = (double)y[t];
            double lt = (double)y[t-1];
            sum_y     += yt;
            sum_lag   += lt;
            sum_lag2  += lt*lt;
            sum_y_lag += yt*lt;
        }
        double T = (double)(n - 1);
        double denom = (T*sum_lag2 - sum_lag*sum_lag);
        double b = 0.0, a = 0.0;
        if (fabs(denom) > 1e-12) {
            b = (T*sum_y_lag - sum_lag*sum_y) / denom;
            a = (sum_y - b*sum_lag) / T;
        } else {
            a = sum_y / T; b = 0.0;
        }
        double pred = a + b * (double)y[n-1];
        if (pred < 0.0) pred = 0.0;
        if (pred > 1.0) pred = 1.0;
        out[d] = pred;
    }
}

static void combine_scores(const double f[], const double ma[], const double ar[],
                           double wf, double wm, double wa, double score[]) {
    for (int d = 0; d < NUM_DEZENAS; ++d)
        score[d] = wf*f[d] + wm*ma[d] + wa*ar[d];
}

static void pick_top_k(const double score[], int k, int out_nums[]) {
    double pairs[NUM_DEZENAS][2];
    for (int d = 0; d < NUM_DEZENAS; ++d) {
        pairs[d][0] = score[d];
        pairs[d][1] = (double)(d+1);
    }
    qsort(pairs, NUM_DEZENAS, sizeof(pairs[0]), cmp_desc_pair);
    for (int i = 0; i < k; ++i) out_nums[i] = (int)(pairs[i][1]);
    // ordena o bilhete final crescente
    for (int i = 0; i < k-1; ++i)
        for (int j = i+1; j < k; ++j)
            if (out_nums[j] < out_nums[i]) { int tmp = out_nums[i]; out_nums[i] = out_nums[j]; out_nums[j] = tmp; }
}

static void diversify(const double base_score[], int k, int n_extra, double jitter, int out[][NUM_BALLS]) {
    for (int e = 0; e < n_extra; ++e) {
        double s[NUM_DEZENAS];
        for (int d = 0; d < NUM_DEZENAS; ++d) {
            double r = ((double)rand() / (double)RAND_MAX);
            double z = sqrt(-2.0 * log(r > 1e-12 ? r : 1e-12)) * cos(2.0*M_PI*((double)rand()/RAND_MAX));
            s[d] = base_score[d] + jitter*z;
        }
        pick_top_k(s, NUM_BALLS, out[e]);
    }
}

int main(int argc, char **argv) {
    const char *csv = NULL;
    int W = 30;
    double wf = 0.30, wm = 0.40, wa = 0.30;
    int n_extra = 3;

    for (int i = 1; i < argc; ++i) {
        if (!strcmp(argv[i], "--csv") && i+1 < argc) csv = argv[++i];
        else if (!strcmp(argv[i], "--window") && i+1 < argc) W = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--wf") && i+1 < argc) wf = atof(argv[++i]);
        else if (!strcmp(argv[i], "--wm") && i+1 < argc) wm = atof(argv[++i]);
        else if (!strcmp(argv[i], "--wa") && i+1 < argc) wa = atof(argv[++i]);
        else if (!strcmp(argv[i], "--extras") && i+1 < argc) n_extra = atoi(argv[++i]);
    }
    if (!csv) {
        fprintf(stderr, "Uso: %s --csv dados.csv [--window W] [--wf] [--wm] [--wa] [--extras N]\n", argv[0]);
        return 1;
    }

    int raw[MAX_DRAWS][NUM_BALLS];
    int n = read_csv(csv, raw);
    if (n <= 0) { fprintf(stderr, "Erro ao ler CSV.\n"); return 1; }

    Indicator ind;
    build_indicator(raw, n, &ind);

    double f[NUM_DEZENAS], ma[NUM_DEZENAS], ar[NUM_DEZENAS], score[NUM_DEZENAS];
    freq_historica(&ind, f);
    media_movel_last(&ind, W, ma);
    ar1_forecast(&ind, ar);
    combine_scores(f, ma, ar, wf, wm, wa, score);

    int principal[NUM_BALLS];
    pick_top_k(score, NUM_BALLS, principal);

    printf("\n=== Mega-Sena — Heuristica (freq + MM%d + AR1) ===\n", W);
    printf("Concursos lidos: %d\n", n);
    printf("Pesos: wf=%.2f wm=%.2f wa=%.2f\n", wf, wm, wa);

    printf("\nPalpite principal: ");
    for (int i = 0; i < NUM_BALLS; ++i) printf("%02d%s", principal[i], (i==NUM_BALLS-1?"\n":" "));
    
    srand((unsigned)time(NULL));
    if (n_extra > 0) {
        int extras[n_extra][NUM_BALLS];
        diversify(score, NUM_BALLS, n_extra, 0.05, extras);
        for (int e = 0; e < n_extra; ++e) {
            printf("Variacao #%d: ", e+1);
            for (int i = 0; i < NUM_BALLS; ++i) printf("%02d%s", extras[e][i], (i==NUM_BALLS-1?"\n":" "));
        }
    }

    printf("\nAviso: heuristica didatica (probabilidades + AR). Loteria e essencialmente aleatoria.\n");
    return 0;
}
