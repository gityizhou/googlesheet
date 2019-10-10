import pygsheets

c = pygsheets.authorize()
s = c.open('Example solar calcs')
ws = s.worksheet('title', 'real_data')


# ws.update_col(2 , ["helloworld"], row_offset=2)
# ws.insert_rows(2, number=2, values=["hellohellohello", "hhhh"], inherit=False)

ws.append_table(["helloworld1"], start='A1', end=None, dimension='ROWS', overwrite=False)
ws.append_table(["helloworld2"], start='A1', end=None, dimension='ROWS', overwrite=False)
