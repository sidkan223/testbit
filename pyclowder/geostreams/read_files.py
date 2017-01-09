import datetime
import logging

from openpyxl import load_workbook


def read_xlsx(file_path):
    logging.info("[pyG.read_files] Loading " + str(file_path))
    wb = load_workbook(file_path, data_only=True,read_only=True)  
    sheet_names = wb.get_sheet_names()
    sheet = wb.get_sheet_by_name(sheet_names[0])
    logging.info("[pyG.read_files] Done loading " + str(file_path))
    
    ### GET THE COLUMN NAMES WHICH ARE LOCATED IN THE FIRST ROW ########################################
    logging.info("[pyG.read_files] getting column headers")
    column_names = []
    i=1
    j=1
    while(1):
        value = sheet.cell(row = i, column = j).value
        if value==None:                                         ### READ ROW UNTIL CELL IS EMPTY -> RETURNS None
            break
        column_names.append(value)
        j += 1
 
    num_cols = len(column_names)

    ### GET THE FIELD VALUES WHICH START IN THE SECOND ROW ########################################
    logging.info("[pyG.read_files] loading data into list")
    field_values = []
    i=2
    count = 0
    while(1):
        count+=1
        #if 500%count==0:
        logging.info("[pyG.read_files] Loaded data row " + str(count))
        j=1
        try:
            value = sheet.cell(row = i, column = j).value  
        except:
            break     
        field_row = []
        while(1):
            if j==num_cols+1:                    
                break
            value = sheet.cell(row = i, column = j).value
            if isinstance(value,datetime.date) or isinstance(value,datetime.time):
                value = str(value)
            field_row.append(value)
            j += 1
        if all(v is None for v in field_row):
            break
        field_values.append(field_row)
        i+=1
    logging.info("[pyG.read_files] Done loading data into list")
    return column_names,field_values

def read_tsv(file_path):
    input_file = open(file_path,'r')
    raw_text = input_file.read()

    ### READ DATA INTO ROWS EXCLUDING LINES STARTING WITH '#'
    rows = []
    line_text = ""

    for i in range(len(raw_text)):
        if raw_text[i] != "\n":

            line_text += raw_text[i]
        else:
            if line_text[0] != "#":
                rows.append(line_text)
            line_text = ""

    headers = rows.pop(0).split("\t")

    logging.info("[pyG.read_files] Creating 2D list of data")
    data = []
    while len(rows) > 0:
        data.append(rows.pop(0).split("\t"))
    del raw_text
    del rows
    logging.info("[pyG.read_files] Done Creating 2D list of data")

    return headers, data

def text2list_noaa(response_in):
    data_out = []
    column_names = []
    header_names = []
    for key in response_in:
        rows = []
        data_site = []
        lineOfText = ""
        for i in range(len(response_in[key])):
            if response_in[key][i] != "\n":
                lineOfText += response_in[key][i]
            else:
                rows.append(lineOfText)
                lineOfText  = ""
        header_text = rows.pop(0)
        header_names = header_text.split("\t")
        header_names.pop(1)
        for i in range(len(rows)):
            data_site.append(rows[i].split("\t"))
            station_text = data_site[i][0].split(":")
            data_site[i][0] = station_text[len(station_text)-1]
            sensor_text = data_site[i][1].split(":")
            data_site[i][1] = sensor_text[len(sensor_text)-2]

            if data_site[i][0] != data_site[i][1]:
                print "Station ID and Sensor ID do not match"
                quit()
            else:
                data_site[i].pop(0)

            # added for water level which has a datum_id for the reference water level
            if len(header_names) > 5:
                if header_names[5] == "datum_id":
                    datum_id_text = data_site[i][5].split(":")
                    data_site[i][5] = datum_id_text[len(datum_id_text)-1]



        header_names[0] = u"station_id"

#TODO: as is, this only processes 1 parameter, needs to be changed to put multiple paratmeters into data_out

    return data_site, header_names






### READ DATA INTO ROWS
# TEMP
#     if("temperature" in values_used):
#         rows_temperature = []
#         lineOfText = ""
#         for i in range(len(temperature_text)):
#             if temperature_text[i] != "\n":
#                 lineOfText += temperature_text[i]
#             else:
#                 rows_temperature.append(lineOfText)
#                 lineOfText  = ""
#         header_text_temperature = rows_temperature.pop(0)
#
# # SALINITY
#     if("salinity" in values_used):
#         rows_salinity = []
#         lineOfText = ""
#         for i in range(len(salinity_text)):
#             if salinity_text[i] != "\n":
#                 lineOfText += salinity_text[i]
#             else:
#                 # if lineOfText[0] != "#":
#                 rows_salinity.append(lineOfText)
#                 lineOfText  = ""
#         header_text_salinity = rows_salinity.pop(0)
#
# # CONDUCTIVITY
#     if("conductivity" in values_used):
#         rows_electrical_conductivity = []
#         lineOfText = ""
#         for i in range(len(conductivity_text)):
#             if conductivity_text[i] != "\n":
#                 lineOfText += conductivity_text[i]
#             else:
#                 # if lineOfText[0] != "#":
#                 rows_electrical_conductivity.append(lineOfText)
#                 lineOfText  = ""
#         header_text_electrical_conductivity = rows_electrical_conductivity.pop(0)
#
#     temperature_data = []
#     salinity_data = []
#     conductivity_data = []
#
#     # station_id, sensor_id, latitude, longitude, time, measurement (C, psu, mS/cm)
#     if("temperature" in values_used):
#         for i in range(len(rows_temperature)):
#             temperature_data.append(rows_temperature[i].split("\t"))
#             station_text = temperature_data[i][0].split(":")
#             temperature_data[i][0] = station_text[len(station_text)-1]
#             sensor_text = temperature_data[i][1].split(":")
#             temperature_data[i][1] = sensor_text[len(sensor_text)-2]
#
#             if temperature_data[i][0] != temperature_data[i][1]:
#                 print "Station ID and Sensor ID do not match"
#                 quit()
#             else:
#                 temperature_data[i].pop(0)
#
#     if("salinity" in values_used):
#         for i in range(len(rows_salinity)):
#             salinity_data.append(rows_salinity[i].split("\t"))
#             station_text = salinity_data[i][0].split(":")
#             salinity_data[i][0] = station_text[len(station_text)-1]
#             sensor_text = salinity_data[i][1].split(":")
#             salinity_data[i][1] = sensor_text[len(sensor_text)-2]
#
#             if salinity_data[i][0] != salinity_data[i][1]:
#                 print "Station ID and Sensor ID do not match"
#                 quit()
#             else:
#                 salinity_data[i].pop(0)
#                 salinity_data[i].insert(4,'')
#
#     if("conductivity" in values_used):
#         for i in range(len(rows_electrical_conductivity)):
#             conductivity_data.append(rows_electrical_conductivity[i].split("\t"))
#             station_text = conductivity_data[i][0].split(":")
#             conductivity_data[i][0] = station_text[len(station_text)-1]
#             sensor_text = conductivity_data[i][1].split(":")
#             conductivity_data[i][1] = sensor_text[len(sensor_text)-2]
#
#             if conductivity_data[i][0] != conductivity_data[i][1]:
#                 print "Station ID and Sensor ID do not match"
#                 quit()
#             else:
#                 conductivity_data[i].pop(0)
#                 conductivity_data[i].insert(4,'')
#                 conductivity_data[i].insert(4,'')
#
# #TODO: if conductivity is used and salinity is not, the indexing will be wrong
#     if("salinity" in values_used):
#         for i in range(len(salinity_data)):
#             match_found = False
#             for j in range(len(temperature_data)):
#                 if temperature_data[j][0] == salinity_data[i][0] \
#                             and temperature_data[j][3] == salinity_data[i][3]:
#                     match_found = True
#                     temperature_data[j].append(salinity_data[i][5])
#             if match_found == False:
#                 temperature_data.append(salinity_data[i])
#
#         for i in range(len(temperature_data)):
#             if len(temperature_data[i]) == 5:
#                 temperature_data[i].append("")
#
#     if("conductivity" in values_used):
#         for i in range(len(conductivity_data)):
#             match_found = False
#             for j in range(len(temperature_data)):
#                 if temperature_data[j][0] == conductivity_data[i][0] \
#                             and temperature_data[j][3] == conductivity_data[i][3]:
#                     match_found = True
#                     temperature_data[j].append(conductivity_data[i][6])
#             if match_found == False:
#                 temperature_data.append(conductivity_data[i])
#
#         for i in range(len(temperature_data)):
#             if len(temperature_data[i]) == 6:
#                 temperature_data[i].append("")
#
#     column_names = ["sea_water_temperature","sea_water_salinity","sea_water_electrical_conductivity"]




# def read_tsv(file_path):
#     input_file = open(file_path,'r')
#     raw_text = input_file.read()

#     ### READ DATA INTO ROWS EXCLUDING LINES STARTING WITH '#'
#     rows = []
#     line_text = ""

#     for i in range(len(raw_text)):
#         if raw_text[i] != "\n":
#             line_text += raw_text[i]
#         else:
#             if line_text[0] != "#":
#                 rows.append(line_text)
#             line_text = ""

#     headers = rows.pop(0).split("\t")

#     logging.info("[pyG.read_files] Creating 2D list of data")
#     data = []
#     while len(rows) > 0:
#         data.append(rows.pop(0).split("\t"))
#     del raw_text
#     del rows
#     logging.info("[pyG.read_files] Done Creating 2D list of data")

# # #COMBINE TIME (field_data[i][2]) AND TIMEZONE (field_data[i][3]) INTO ONE FIELD (field_data[i][2])
# #     for i in range(len(field_data)):
# #         field_data[i][2] = time_transform(field_data[i][2],field_data[i][3])
# #         field_data[i].pop(3)

#     return headers, data