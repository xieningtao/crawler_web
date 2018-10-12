# encoding:UTF-8
def yield_test(n):
    for i in range(n):
        yield call(i)


        print("i=", i)
        # 做一些其它的事情
    print("do something.")
    print("end.")


def call(i):
    return i * 2


# 使用for循环
total = yield_test(5)

#这个时候才开始执行
print(total.next(),"total")

print(total.next(),"total2")
# for i in total:
#     print(i, ",")
