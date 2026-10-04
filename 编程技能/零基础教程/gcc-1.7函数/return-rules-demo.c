#include <stdio.h>

/* 1.7 第 2 课 · return 的 3 条规则 + 3 种调用方式
   目的：用【可跑代码】证明规则，不许「看形式猜」
*/

/* ══ 规则 1：一次只能返回一个值 ══ */
int tryReturnTwo(int a, int b) {
    return a;      /* ← 执行到这里就结束了 */
    return b;      /* ← 这行【永远不执行】 */
}

/* ══ 规则 2：return 后面的代码不执行 ══ */
int showOrder() {
    printf("   ① 进函数\n");
    return 10;
    printf("   ② 这行【永远不执行】\n");   /* 编译器会警告 */
}

/* ══ 规则 3：返回值类型要和函数类型一致 ══ */
int typeMismatch() {
    return 3.99;   /* ← 函数是 int，返回小数 ⇒ 被【截断】成 3 */
}

/* ══ 3 种调用方式 ══ */
void printStar() {
    printf("   *****\n");
}

int max(int a, int b) {
    return a > b ? a : b;
}

int max3(int a, int b, int c) {
    return max(max(a, b), c);      /* 嵌套调用 */
}

int main() {
    printf("=== 规则 1：一次只能返回一个值 ===\n");
    printf("   tryReturnTwo(7, 99) = %d  ← 只返回了第一个\n", tryReturnTwo(7, 99));

    printf("\n=== 规则 2：return 后面的代码不执行 ===\n");
    printf("   返回值 = %d\n", showOrder());

    printf("\n=== 规则 3：返回值类型要匹配 ===\n");
    printf("   typeMismatch() = %d  ← 3.99 被截断成 3\n", typeMismatch());

    printf("\n=== 3 种调用方式 ===\n");
    printf("   ① 函数语句：\n");
    printStar();                                  /* ① 函数语句 */
    int c = 2 * max(3, 5);
    printf("   ② 函数表达式：2 * max(3,5) = %d\n", c);
    printf("   ③ 函数参数：printf 里直接调 max ⇒ %d\n", max(3, 5));

    printf("\n=== 嵌套调用 ===\n");
    printf("   max3(3, 7, 5) = %d\n", max3(3, 7, 5));
    printf("   执行顺序：main → max3 → max(3,7)=7 → max(7,5)=7 → main\n");

    return 0;
}
