import pandas as pd

def get_column_index(df, column_name):
    return df.columns.get_loc(column_name)

def process_df(df, start_row, end_row, start_col, end_col, layer):
    space = "    " * layer
    if layer > 10:
        print("递归太深.")
        return
    while start_row < end_row:
        if start_col < end_col:
            name = df.iloc[start_row, start_col]
            type = df.iloc[start_row, start_col + 1]
            length = df.iloc[start_row, start_col + 2]
            # int 类型
            if type != 'struct' and length == 1:
                print(f"{space}.{name} = {df.iloc[start_row]['value']}")
                start_row += 1
                if start_row > end_row:
                    return
            # 数组类型
            elif type != 'struct' and length > 1:
                print(f"{space}.{name} =")
                print(f"{space}{{")
                while length > 0:
                    print(f"{space}{df.iloc[start_row]['value']}")
                    length -= 1
                    start_row += 1
                print(f"{space}}}, ")
                if start_row > end_row:
                    return
            # 结构体类型
            elif type == 'struct':
                print(f"{space}.{name} =")
                print(f"{space}{{")
                layer += 1
                # 查询结构体结束行的index
                i = start_row + 1
                while i < end_row:
                    if isinstance(df.iloc[i, start_col], str):
                        break
                    else:
                        i += 1
                process_df(df, start_row, i, start_col + 3, end_col, layer)
                layer -= 1
                start_row += int(length)
                print(space + '}')
        else:
            return



if __name__ == '__main__':
    df = pd.read_excel('demo.xlsx', sheet_name='Sheet1')
    end_col = df.columns.get_loc('mean')
    layer = 0
    process_df(df, 0, len(df), 0, end_col, layer)
    