#include <stdio.h>
int main(void) {
    int i, s = 0;
    for (i = 1; i <= 5; i++) {
        if (i == 3) continue;
        s = s + i;
    }
    printf("%d %d\n", s, i);

    int j, t = 0;
    for (j = 1; j <= 5; j++) {
        if (j == 3) break;
        t = t + j;
    }
    printf("%d %d\n", t, j);
    return 0;
}
