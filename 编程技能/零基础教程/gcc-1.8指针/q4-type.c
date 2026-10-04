int main() {
    int  a = 10;
    char c = 'A';
    int  *p = &a;    /* ✅ int* 盒 ← int 编号 */
    char *q = &c;    /* ✅ char* 盒 ← char 编号 */
    /* p = &c;  ❌ int* 盒 ← char 编号（类型不符）*/
    /* q = &a;  ❌ char* 盒 ← int 编号（类型不符）*/
    return 0;
}
