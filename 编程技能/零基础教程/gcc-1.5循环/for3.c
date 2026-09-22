#include <stdio.h>

int main(void) {
    /* A: 无分号，循环体就是 s=s+1，跑 3 圈 */
    int i, s = 0;
    for (i = 1; i <= 3; i++)
        s = s + 1;
    printf("A: %d %d\n", s, i);

    /* B: 有分号，大括号掉到循环外 */
    int i2, s2 = 0;
    for (i2 = 1; i2 <= 3; i2++);
    {
        s2 = s2 + 1;
    }
    printf("B: %d %d\n", s2, i2);

    /* C: 无分号，5 圈 */
    int i3, s3 = 0;
    for (i3 = 1; i3 <= 5; i3++)
        s3 = s3 + 1;
    printf("C: %d %d\n", s3, i3);

    /* D: 有分号，5 圈 */
    int i4, s4 = 0;
    for (i4 = 1; i4 <= 5; i4++);
    {
        s4 = s4 + 1;
    }
    printf("D: %d %d\n", s4, i4);

    /* E: 无分号但循环体只有一行 printf，直接看印几次 */
    printf("E: ");
    for (int k = 1; k <= 3; k++)
        printf("[%d]", k);
    printf("\n");

    return 0;
}
