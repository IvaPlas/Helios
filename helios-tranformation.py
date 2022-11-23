import pandas as pd
import xml.etree.cElementTree as ET
# from xml.dom import minidom  # for prettify


helios_file = 'data/excel/sklad_helios.xlsx'
alza_xml_file = 'data/exports/alza_export.xml'
czc_xml_file = 'data/exports/czc_export.xml'

print('~~~~~~~~~~~~~~~~~~~~~~~~~')
print('~~~ HELIOS XML EXPORT ~~~')
print('~~~~~~~~~~~~~~~~~~~~~~~~~')

helios_data = pd.read_excel(helios_file, dtype={'Čárový kód': object})  # to keep leading zeros in EAN
print(helios_data.head(11))


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
        AUTHOR_FEE = str(row['CopyrightFee'])
        if '.' in AUTHOR_FEE:
            AUTHOR_FEE = AUTHOR_FEE.replace('.', ',')
        RECYCLE_FEE = str(row['JC hist. recykl. přísp.'])
        if '.' in RECYCLE_FEE:
            RECYCLE_FEE = RECYCLE_FEE.replace('.', ',')
        WEIGHT_BRUTTO = str(row['Hmotnost'])
        if '.' in WEIGHT_BRUTTO:
            WEIGHT_BRUTTO = WEIGHT_BRUTTO.replace('.', ',')
        SIZE_X_NETTO = str(row['Šířka'])
        if '.' in  SIZE_X_NETTO:
            SIZE_X_NETTO =  SIZE_X_NETTO.replace('.', ',')
        SIZE_Y_NETTO = str(row['Výška'])
        if '.' in SIZE_Y_NETTO:
            SIZE_Y_NETTO = SIZE_Y_NETTO.replace('.', ',')
        SIZE_Z_NETTO = str(row['Hloubka'])
        if '.' in SIZE_Z_NETTO:
            SIZE_Z_NETTO = SIZE_Z_NETTO.replace('.', ',')
        WARRANTY = row['WARRANTY']


        shopitem = ET.SubElement(root, "Shopitem")
        ET.SubElement(shopitem, "CODE").text = str(CODE)
        ET.SubElement(shopitem, "ESHOP_CODE").text = str(ESHOP_CODE)
        ET.SubElement(shopitem, "Name").text = str(Name)
        ET.SubElement(shopitem, "Ean").text = str(Ean)
        ET.SubElement(shopitem, "Price").text = str(Price)
        ET.SubElement(shopitem, "Quantity").text = str(Quantity)
        ET.SubElement(shopitem, "MANUFACTURER").text = str(MANUFACTURER)
        ET.SubElement(shopitem, "IMAGE").text = str(IMAGE)
        ET.SubElement(shopitem, "URL").text = str(URL)
        ET.SubElement(shopitem, "DESCRIPTION").text = str(DESCRIPTION)
        ET.SubElement(shopitem, "CURRENCY").text = str(CURRENCY)
        ET.SubElement(shopitem, "AUTHOR_FEE").text = AUTHOR_FEE
        ET.SubElement(shopitem, "RECYCLE_FEE").text = RECYCLE_FEE
        ET.SubElement(shopitem, "WEIGHT_BRUTTO").text = WEIGHT_BRUTTO
        ET.SubElement(shopitem, "SIZE_X_NETTO").text = SIZE_X_NETTO
        ET.SubElement(shopitem, "SIZE_Y_NETTO").text = SIZE_Y_NETTO
        ET.SubElement(shopitem, "SIZE_Z_NETTO").text = SIZE_Z_NETTO
        ET.SubElement(shopitem, "WARRANTY").text = str(WARRANTY)


    return root

# create full alza_xml.xml
root_alza = ET.Element("items")
root_czc = ET.Element("shop")

for i, row in helios_data.iterrows():
    root_czc = get_product_xml(row, root_czc, type_='czc')
    root_alza = get_product_xml(row, root_alza, type_='alza')
print(root_czc)
# export xmls
ET.ElementTree(root_alza).write(alza_xml_file)
ET.ElementTree(root_czc).write(czc_xml_file)

