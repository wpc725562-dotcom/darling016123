#include <stdio.h>

int main(void) {
    /* Q1: for 末尾多一个分号，且循环体没有大括号 */
    int i, s = 0;
    for (i = 1; i <= 3; i++);
    printf("%d %d\n", s, i);

    /* Q1 对照：去掉那个分号，其余一字不改 */
    int i2, s2 = 0;
    for (i2 = 1; i2 <= 3; i2++)
        s2 = s2 + i2;
    printf("%d %d\n", s2, i2);

    /* Q1 对照 2：分号后面跟大括号 —— 大括号被当成循环体了吗 */
    int i3, s3 = 0;
    for (i3 = 1; i3 <= 3; i3++);
    {
        s3 = s3 + 1;
    }
    printf("%d %d\n", s3, i3);

    return 0;
}
