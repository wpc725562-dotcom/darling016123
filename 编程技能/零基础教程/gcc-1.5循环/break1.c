#include <stdio.h>

int main(void) {
    /* B1: break —— 到 3 就整个跳出 */
    printf("B1: ");
    for (int i = 1; i <= 5; i++) {
        if (i == 3) break;
        printf("%d", i);
    }
    printf("\n");

    /* B2: continue —— 跳过 3，其余照印 */
    printf("B2: ");
    for (int i = 1; i <= 5; i++) {
        if (i == 3) continue;
        printf("%d", i);
    }
    printf("\n");

    /* B3: break 出去后 i 停在哪 */
    int i3;
    for (i3 = 1; i3 <= 5; i3++) {
        if (i3 == 3) break;
    }
    printf("B3: break 出去后 i3 = %d\n", i3);

    /* B4: 正常跑完 i 停在哪（对照） */
    int i4;
    for (i4 = 1; i4 <= 5; i4++) {
        if (i4 == 9) break;
    }
    printf("B4: 正常跑完 i4 = %d\n", i4);

    /* B5: while 里 continue 写在推进之前 → 推进被跳过，卡死 */
    printf("B5: ");
    int m = 1, guard = 0;
    while (m <= 5) {
        guard++;
        if (guard > 5) { printf("(卡死！m 一直是 %d)", m); break; }
        if (m == 3) continue;
        printf("%d", m);
        m++;
    }
    printf("\n");

    /* B6: 把推进补在 continue 之前 → 正常 */
    printf("B6: ");
    int n = 1;
    while (n <= 5) {
        if (n == 3) { n++; continue; }
        printf("%d", n);
        n++;
    }
    printf("\n");

    return 0;
}
