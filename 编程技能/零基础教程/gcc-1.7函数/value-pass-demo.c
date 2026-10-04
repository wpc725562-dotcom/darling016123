#include <stdio.h>

/* 1.7 第 1 课 · 值传递验证
   目的：证明「函数里改了形参，外面的实参【不变】」
   —— 用【具体数字】说话，不许「看形式猜」
*/

void tryChange(int x) {
    printf("   进入函数时：x = %d\n", x);
    x = 999;                                  /* 改形参 */
    printf("   改完之后：  x = %d  ← 函数里的 x 变了\n", x);
}

int addTwo(int a, int b) {                    /* 形参：a, b */
    return a + b;
}

void printArray(int arr[], int n) {           /* 数组传参 */
    printf("   函数里看到的数组：");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");
    arr[0] = 999;                             /* ⚠️ 改数组元素 */
}

int main() {
    printf("=== 实验 1：值传递（普通变量）===\n");
    int a = 10;
    printf("   调用前：a = %d\n", a);
    tryChange(a);
    printf("   调用后：a = %d  ← 【没变！】\n", a);
    printf("   ⇒ 结论：形参是实参的【复印件】，改复印件不影响原件\n");

    printf("\n=== 实验 2：形参 vs 实参（名字可以不一样）===\n");
    int m = 3, n = 5;
    printf("   实参：m = %d, n = %d\n", m, n);
    int s = addTwo(m, n);                     /* 实参：m, n */
    printf("   返回：%d\n", s);
    printf("   ⇒ 形参叫 a,b；实参叫 m,n —— 【名字无关】，按【位置】对应\n");

    printf("\n=== 实验 3：数组传参（⚠️ 这里会变！）===\n");
    int arr[3] = {1, 2, 3};
    printf("   调用前：arr[0] = %d\n", arr[0]);
    printArray(arr, 3);
    printf("   调用后：arr[0] = %d  ← 【变了！】\n", arr[0]);
    printf("   ⇒ 为什么？因为数组名传的是【地址】（1.8 指针会讲）\n");

    return 0;
}
