def masuk_tweet(StoreData):

    sd = StoreData
    hst = None
    hs = []

    for i in range(0,len(sd)-1):
        hs.append(sd.iloc[i,4])
    
    #if hs is list:
"""
    for i in hs:
        sql = "
        
        INSERT INTO `hashtag` (`isi`) 
            SELECT * FROM (SELECT %s) AS tmp
            WHERE NOT EXISTS (
                SELECT 'isi' FROM `hashtag` 
                WHERE `isi` = '%s'
                ) LIMIT 1;   
        "
        
        hst = cursor.execute(sql, [i])
        print(hst)
        print(cursor.lastrowid)
        con.commit()
"""

"""            
    for a in range(0,len(sd)-1):
        
        sql2 = "INSERT INTO `tweet` (`idH`, `tweet`, `Username`, `RT`, `SA`) VALUES (%s, %s, %s, %s, %s);"
                        
        cursor.execute(sql2,(
        
        sd.iloc[a,3],
        sd.iloc[a,1], 
        sd.iloc[a,5], 
        sd.iloc[a,6]))
        
        con.commit()
"""
        
"""
        if hst == None:
            sql = "    
            SELECT * 
            FROM `hashtag` 
            WHERE `isi` = %s;     
            "
            cursor.execute(sql, i)

        else:
"""    
            
"""
    else:
        sql = "
        SELECT * 
        FROM `hashtag` 
        WHERE `isi` = %s;     
        "
        #for a in hs:
        hst = cursor.execute(sql,hs)
            #print(a)
"""
            
        #con.commit()
def has_dup(StoreData):
    sd = StoreData
    unique = []
    hs = []
    for i in range(0, len(sd)-1):    
        hs.extend([sd.iloc[i,4]])

    a = []
    index = -1
    for i in hs:
        j = []
        index += 1
        if len(i.split(' ')) > 2 :
            for z in i.split(' '):
                #print(z)
                j.append(z)
                #print(j)
            hs[index] = (i.split(' '))[0]   
        a.extend(j)
    #print(a)
    hs.extend(a)
    #print(hs)
    
    
    for hashtag in hs: 
            if hashtag not in unique: 
                unique.append(hashtag) 
            #return unique
        #print(sd.iloc[i,4])
    return unique    
 

def bakuprt():
  for a in range(0,len(sdr)-1):
        
        sqlrt = """
        Select `idR` FROM `retweet` WHERE `retweet` = %s 
        """ # get idT dari tabel tweet

        cursor.execute(sqlrt, sdr.iloc[a, 3])
        hidt = cursor.fetchall()
        #print(len(hidt))

       #print("hasil rt = ", len(hidt))

        if len(hidt) > 0:
            pass 

        else:
            #input_retweet(sd, a, hidt)
            sqlrti = """
            Select `idT` FROM `tweet` WHERE `tweet`.`idJsonT` = 
            (SELECT `idJsonR` FROM `retweet`)
            """
            cursor.execute(sqlrti)
            hasrti = cursor.fetchall()
            
            #print("hasil idJson = ", len(hasrti))

            if len(hasrti) > 0:
                input_retweet(sdr, a, hasrti)

                
            else:
                sqli = """
                INSERT INTO `tweet` 
                (`idT`, `idJsonT`, `tweet`, `tanggal`, `Username`, `RT`, `SA`) 
                SELECT `idR`, `idJsonR`, `retweet`, `tanggal`, `Username`, `RT`, `SA`
                FROM `retweet`;
                """
                cursor.execute(sqli)
                con.commit()
            
            sqlrtj = """
            Select `idT` FROM `tweet` WHERE `tweet`.`idJsonT` = 
            (SELECT `idJsonR` FROM `retweet`)
            """
            cursor.execute(sqlrtj)
            hasrtij = cursor.fetchall()
            
            if len(hasrtij) > 0:
                input_retweet(sdr, a, hasrtij)

            else:
                pass
            
                        