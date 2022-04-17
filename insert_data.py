import sqlite3
con = sqlite3.connect('data.db')

cur = con.cursor()

cur.execute("INSERT INTO user VALUES (3, 'testing', 'test', 1, 0, '123 lane', 'test', 'test', 'city', 'test@gmail.com')")

cur.execute("INSERT INTO warning VALUES (1, 'This is a test warning')")
cur.execute("INSERT INTO warning VALUES (2, 'This item is selling fast')")
cur.execute("INSERT INTO warning VALUES (3, 'This item maybe slow to ship')")

cur.execute("INSERT INTO item VALUES (1, 2, 2, 999, 'This item is a brand new iphone. Its amazing', 'https://m.media-amazon.com/images/I/61s0IaMcKtL._AC_SL1500_.jpg', 1, 'new phone')")
cur.execute("INSERT INTO item VALUES (2, 2, 2, 99, 'This item is a brand new candle. Its amazing', 'https://www.sephora.com/productimages/sku/s1947027-main-zoom.jpg?imwidth=315', 1, 'big candle')")
cur.execute("INSERT INTO item VALUES (3, 2, 2, 200, 'This is the newest and greatest candle of all time', 'http://cdn.shopify.com/s/files/1/0465/1889/4755/files/hotel-lobby-candle-social-image_1200x1200.jpg?v=1642786223', 1, 'Pink Candle')")
cur.execute("INSERT INTO item VALUES (4, 2, 2, 201, 'Sewing kit from the best company in the world', 'https://img.buzzfeed.com/buzzfeed-static/static/2020-05/6/16/asset/7d7e4a28b91b/sub-buzz-1686-1588783092-9.jpg', 1, 'Sewing kit')")
cur.execute("INSERT INTO item VALUES (5, 2, 2, 21, 'Car USB', 'https://cimg2.ibsrv.net/ibimg/hgm/570x321-1/100/338/awful-etsy-car-stuff-volume-1_100338554.jpg', 1, 'USB Drive')")
cur.execute("INSERT INTO item VALUES (6, 2, 2, 21, 'Tree in a dome', 'https://noveltystreet.com/wp-content/uploads/2017/03/Vert-Sauvage-Forest-Terrarium-Of-Artificial-Plants-Pet-Plant.jpg', 1, 'Tree')")
cur.execute("INSERT INTO item VALUES (7, 2, 2, 45, 'Fancy Car Fob', 'https://hip2save.com/wp-content/uploads/2021/12/car-key-covers.jpg?resize=1200%2C990&strip=all', 1, 'Car Fobs')")


# Insert a few rows of data
# cur.execute("INSERT INTO item VALUES ('1', '1', 'My first blog' ,'Some content', 1)")
# cur.execute("INSERT INTO blogs VALUES ('private-blog', '2021-03-07', 'Secret blog' ,'This is a secret', 0)")

# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()