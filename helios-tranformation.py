import pandas as pd
import xml.etree.cElementTree as ET
import numpy as np
# from xml.dom import minidom  # for prettify


helios_file = 'data/excel/sklad_helios.xlsx'
alza_xml_file = 'data/exports/alza_export.xml'
czc_xml_file = 'data/exports/czc_export.xml'

print('~~~~~~~~~~~~~~~~~~~~~~~~~')
print('~~~ HELIOS XML EXPORT ~~~')
print('~~~~~~~~~~~~~~~~~~~~~~~~~')

helios_data = pd.read_excel(helios_file, dtype={'Čárový kód': object})  # to keep leading zeros in EAN
print(helios_data.head(11))


def handle_nan(value, round_=False):
    if isinstance(value, (int, float)):  # int / float
        if np.isnan(value):
            return ''
        else:
            if round_ is True:
                return str(round(value))
            else:
                if '.' in str(value):
                    if value == 0 or str(value) == "0.0":
                        return "0"
                    else:
                        return str(value).replace('.', ',')
                else:
                    return str(value)
    else:  # value is string
        if int(value) == 0:
            return "0"
        else:
            return str(value)

def get_product_xml(row, root, type_):



    if type_ == 'alza':

        PriceWithFee = row['Alternativní cena']
        PriceWithoutFee = row['PriceWithoutFee']
        VAT = row['VAT']
        RecycleFee = str(row['JC hist. recykl. přísp.'])
        if '.' in RecycleFee:
            RecycleFee = RecycleFee.replace('.', ',')
        CopyrightFee = row['CopyrightFee']
        Currency = row['Currency']
        StoredQuantity = row['Množství skladem']
        Name = row['Název 1']  #.encode('utf8')
        DealerCode = row['Registrační číslo']
        PartNumber = row['PartNumber']
        Ean = row['Čárový kód']

        item = ET.SubElement(root, "item")
        pricing = ET.SubElement(item, "Pricing")
        ET.SubElement(pricing, "PriceWithFee").text = str(round(PriceWithFee))
        ET.SubElement(pricing, "PriceWithoutFee").text = str(round(PriceWithoutFee))
        ET.SubElement(pricing, "VAT").text = str(VAT)
        ET.SubElement(pricing, "RecycleFee").text = RecycleFee
        ET.SubElement(pricing, "CopyrightFee").text = str(CopyrightFee)
        ET.SubElement(pricing, "Currency").text = str(Currency)
        storage = ET.SubElement(item, "Storage")
        ET.SubElement(storage, "StoredQuantity").text = str(StoredQuantity)
        product = ET.SubElement(item, "Product")
        ET.SubElement(product, "Name").text = str(Name)
        ET.SubElement(product, "DealerCode").text = str(DealerCode)
        ET.SubElement(product, "PartNumber").text = str(PartNumber)
        ET.SubElement(product, "Ean").text = str(Ean)

    elif type_ == 'czc':

        CODE = row['Registrační číslo']
        ESHOP_CODE = row['Registrační číslo']
        Name = row['Název 1']  # .encode('utf8')
        Ean = row['Čárový kód']
        Price = row['Prodejní cena']
        Quantity =row['Množství skladem']
        MANUFACTURER = row['MANUFACTURER']
        IMAGE = row['IMAGE']
        URL = row['URL']
        DESCRIPTION = row['DESCRIPTION']
        CURRENCY = row['Currency']
        AUTHOR_FEE = row['CopyrightFee']
        RECYCLE_FEE = row['JC hist. recykl. přísp.']
        WEIGHT_BRUTTO = row['Hmotnost']
        SIZE_X_NETTO = row['Šířka']
        SIZE_Y_NETTO = row['Výška']
        SIZE_Z_NETTO = row['Hloubka']
        WARRANTY = row['WARRANTY']

        shopitem = ET.SubElement(root, "Shopitem")
        ET.SubElement(shopitem, "CODE").text = str(CODE)
        ET.SubElement(shopitem, "ESHOP_CODE").text = str(ESHOP_CODE)
        ET.SubElement(shopitem, "Name").text = str(Name)
        ET.SubElement(shopitem, "Ean").text = str(Ean)
        ET.SubElement(shopitem, "Price").text = handle_nan(Price, round_=True)
        ET.SubElement(shopitem, "Quantity").text = str(Quantity)
        ET.SubElement(shopitem, "MANUFACTURER").text = handle_nan(MANUFACTURER)
        ET.SubElement(shopitem, "IMAGE").text = handle_nan(IMAGE)
        ET.SubElement(shopitem, "URL").text = handle_nan(URL)
        ET.SubElement(shopitem, "DESCRIPTION").text = handle_nan(DESCRIPTION)
        ET.SubElement(shopitem, "CURRENCY").text = str(CURRENCY)
        ET.SubElement(shopitem, "AUTHOR_FEE").text = handle_nan(AUTHOR_FEE)
        ET.SubElement(shopitem, "RECYCLE_FEE").text = handle_nan(RECYCLE_FEE)
        ET.SubElement(shopitem, "WEIGHT_BRUTTO").text = handle_nan(WEIGHT_BRUTTO)
        ET.SubElement(shopitem, "SIZE_X_NETTO").text = handle_nan(SIZE_X_NETTO)
        ET.SubElement(shopitem, "SIZE_Y_NETTO").text = handle_nan(SIZE_Y_NETTO)
        ET.SubElement(shopitem, "SIZE_Z_NETTO").text = handle_nan(SIZE_Z_NETTO)
        ET.SubElement(shopitem, "WARRANTY").text = handle_nan(WARRANTY)

    return root


# create full alza_xml.xml
root_alza = ET.Element("items")
root_czc = ET.Element("shop")

for i, row in helios_data.iterrows():
    root_czc = get_product_xml(row, root_czc, type_='czc')
    root_alza = get_product_xml(row, root_alza, type_='alza')

# export xmls
ET.ElementTree(root_alza).write(alza_xml_file)
ET.ElementTree(root_czc).write(czc_xml_file)


import ftplib
HOSTNAME = "s5.eshop-rychle.cz"
USERNAME = "12829.s5.eshop-rychle.cz"
PASSWORD = "SuPTyYo751*"

ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
# ftp_server.encoding = "utf-8"

xml_files = [alza_xml_file, czc_xml_file]
# filenames = ['alza_export.xml', 'czc_export.xml']
for xml_file in xml_files:
    filename = xml_file.split('/')[-1]
    print('saving file ...', filename)
    with open(xml_file, "rb") as file:
        ftp_server.storbinary(f"STOR {filename}", file)

ftp_server.dir()
ftp_server.quit()
