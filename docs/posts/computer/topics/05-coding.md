---
title: "考点拆分 05 · 手写编程 + 简答综合（约 60 分）"
description: "2024 真题考点拆分 05 · 手写编程 + 简答综合（约 60 分）· 考试策略 + 系统笔记索引"
---

# 考点拆分 05 · 手写编程 + 简答综合（约 60 分）

> 来源：[2024 回忆版](/posts/computer/2024)  
> 系统笔记：**1.5 循环结构程序设计** **1.6 数组** **2.1 数据结构基本概念** **2.2 线性表** **2.6 图**

---

## 考试策略

1. **先伪代码再落 C**（3 分钟想清输入/输出/循环边界）  
2. 必写：`#include`、`main`、`return 0`、分号、花括号配对  
3. 变量先初始化再累加  
4. 简答写**关键词分点**，不写长段落

---

## 2024 三道编程（必须默写）

### A. 3×3 按行填 201–209
```c
#include <stdio.h>
int main() {
    int a[3][3], num = 201;
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            a[i][j] = num++;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++)
            printf("%d ", a[i][j]);
        printf("\n");
    }
    return 0;
}
```

### B. 30 个成绩找最高分
```c
#include <stdio.h>
int main() {
    int scores[30], max;
    for (int i = 0; i < 30; i++)
        scanf("%d", &scores[i]);
    max = scores[0];
    for (int i = 1; i < 30; i++)
        if (scores[i] > max) max = scores[i];
    printf("最高分 = %d\n", max);
    return 0;
}
```

### C. 1–300 奇偶分别求和
```c
#include <stdio.h>
int main() {
    int sum_odd = 0, sum_even = 0;
    for (int i = 1; i <= 300; i++) {
        if (i % 2) sum_odd += i;
        else sum_even += i;
    }
    printf("奇数和 = %d\n", sum_odd);
    printf("偶数和 = %d\n", sum_even);
    return 0;
}
```
参考：奇数和 22500，偶数和 22650。

---

## 简答默写清单（2024）

| 题 | 关键词（闭卷能写出） |
|:---|:---|
| 数据项 / ADT | 最小单位；模型+操作；抽象/封装；(D,S,P) |
| 程序功能+i | 求平均；i=10 |
| 顺序表优缺点 | 随机O(1)/密度高；插删O(n)/预分配 |
| 有向图出入度 | 有序对；OD/ID；和=边数 |

---

## 编程同型加练（纸上写）

1. 输入 n 个数，输出平均值（保留 1 位小数）  
2. 将一维数组逆序输出  
3. 统计 1–100 中 3 的倍数个数  
4. 输入一行字符串，统计元音字母个数

---

## 勾选

- [ ] A/B/C 三道不看答案默写满分  
- [ ] 4 道简答关键词 5 分钟默完  
- [ ] 同型加练至少 2 道

---

返回：**_索引** · [全卷](/posts/computer/2024)
