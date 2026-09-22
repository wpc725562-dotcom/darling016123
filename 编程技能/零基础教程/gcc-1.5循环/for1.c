#include <stdio.h>

int main(void) {
    /* F1: 最标准的 for —— 起点/条件/推进 全在一行 */
    printf("F1: ");
    for (int i = 1; i <= 5; i++) {
        printf("%d", i);
    }
    printf("\n");

    /* F2: for 末尾多了一个分号 —— 循环体变成空语句 */
    int s2 = 0;
    for (int i = 1; i <= 5; i++);
    {
        s2 = s2 + 100;
    }
    printf("F2: s2 = %d\n", s2);

    /* F2b: 对照 —— 去掉那个分号 */
    int s2b = 0;
    for (int i = 1; i <= 5; i++)
    {
        s2b = s2b + 100;
    }
    printf("F2b: s2b = %d\n", s2b);

    /* F3: 循环结束后，i 停在哪 */
    int i3;
    for (i3 = 1; i3 <= 5; i3++) {
        /* 空 */
    }
    printf("F3: 结束后 i3 = %d\n", i3);

    /* F4: for 与 while 等价改写，同一个任务 */
    printf("F4-for:   ");
    for (int k = 1; k <= 3; k++) printf("%d", k);
    printf("\n");

    printf("F4-while: ");
    int k = 1;
    while (k <= 3) {
        printf("%d", k);
        k++;
    }
    printf("\n");

    /* F5: 三部分全省略 —— 死循环，靠 break 出来 */
    printf("F5: ");
    int n = 0;
    for (;;) {
        n++;
        if (n > 3) break;
        printf("%d", n);
    }
    printf("  (n=%d)\n", n);

    /* F6: 条件一开始就假 —— 一次都不进 */
    printf("F6: ");
    for (int j = 10; j <= 5; j++) printf("%d", j);
    printf("(空)\n");

    return 0;
}
