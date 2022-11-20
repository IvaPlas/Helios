import pandas as pd
import xml.etree.cElementTree as ET
# from xml.dom import minidom  # for prettify


helios_file = 'data/excel/sklad_helios.xlsx'
alza_xml_file = 'data/exports/alza_export.xml'

print('~~~~~~~~~~~~~~~~~~~~~~~~~')
print('~~~ HELIOS XML EXPORT ~~~')
print('~~~~~~~~~~~~~~~~~~~~~~~~~')

helios_data = pd.read_excel(helios_file, dtype={'Čárový kód': object})  # to keep leading zeros in EAN
print(helios_data.head(11))


def get_product_xml(row, items):

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

    item = ET.SubElement(items, "item")
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

    return items


# create full alza_xml.xml
items = ET.Element("items")
for i, row in helios_data.iterrows():
    items = get_product_xml(row, items)

# export xml
tree = ET.ElementTree(items)
tree.write(alza_xml_file)



### string method ###

# def get_product_xml(row):
#
#     PriceWithFee = row['Alternativní cena']
#     PriceWithoutFee = row['PriceWithoutFee']
#     VAT = row['VAT']
#     RecycleFee = str(row['JC hist. recykl. přísp.'])
#     if '.' in RecycleFee:
#         RecycleFee = RecycleFee.replace('.', ',')
#     CopyrightFee = row['CopyrightFee']
#     Currency = row['Currency']
#     StoredQuantity = row['Množství skladem']
#     Name = row['Název 1'].encode('utf8')
#     DealerCode = row['Registrační číslo']
#     PartNumber = row['PartNumber']
#     Ean = row['Čárový kód']
#    # Ean = Ean if np.isnan(Ean) else int(Ean)
#
#     product_xml = '<item>\n<Pricing>\n<PriceWithFee>' + str(round(PriceWithFee)) + \
#                   '</PriceWithFee>\n<PriceWithoutFee>' + str(round(PriceWithoutFee)) + \
#                   '</PriceWithoutFee>\n<VAT>' + str(VAT) + \
#                   '</VAT>\n<RecycleFee>' + RecycleFee + \
#                   '</RecycleFee>\n<CopyrightFee>' + str(CopyrightFee) + \
#                   '</CopyrightFee>\n<Currency>' + str(Currency) + \
#                   '</Currency>\n</Pricing>\n<Storage>\n<StoredQuantity>' + str(StoredQuantity) + \
#                   '</StoredQuantity>\n</Storage>\n<Product>\n<Name>' + str(Name) + \
#                   '</Name>\n<DealerCode>' + str(DealerCode) + \
#                   '</DealerCode>\n<PartNumber>' + str(PartNumber) + \
#                   '</PartNumber>\n<Ean>' + str(Ean) + \
#                   '</Ean>\n</Product>\n</item>'
#
#     return product_xml
#
#
# # create full alza_xml string
# alza_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<items>\n'
# for i, row in helios_data.iterrows():
#     product_xml = get_product_xml(row)
#     alza_xml += product_xml
# alza_xml += '\n\n</items>'
#
# # export file to xml (as text obviously)
# with open(alza_xml_file, 'w') as alza_file:
#     alza_file.write(alza_xml)
#
#     # .replace('/&(?!#?[a-z0-9]+;)/g', '&amp;'))
