length=90560


lengthdy=int(length/86400)
lengthhr=int(int(length-int(lengthdy*86400))/3600)
lengthmin=int(int(length-int(lengthdy*86400)-int(lengthhr*3600))/60)
lengthsec=int(length-int(lengthdy*86400)-int(lengthhr*3600)-int(lengthmin*60))

if len(str(lengthsec)) == 1:
    lengthsec=f"0{lengthsec}"
elif len(str(lengthsec)) == 2:
    lengthsec=f"{lengthsec}"
else:
    lengthsec=f"00"

print(f"{lengthdy} : {lengthhr} : {lengthmin} : {lengthsec}")