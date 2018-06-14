def arc_parse(packet):
  print(packet,'\n')

  if len(packet) == 54:
    print('len data packet 54 \n')
    big_to_little(packet)
    print(packet)
    otv_start = packet[0]
    print('otv start',otv_start,'\n')
    otv_end = packet[1]
    print('otv end',otv_end,'\n')
    start_time = packet[2]|(packet[3]<<8)|(packet[4]<<16)|(packet[5]<<24)
    print('start_time',start_time,'\n')
    flo32 = 0.0 
    value = packet[6]|(packet[7]<<8)|(packet[8]<<16)|(packet[9]<<24)
    flo32 = struct.pack('I',value)
    Summ_Mass_Liquid = struct.unpack('f',flo32)
    print("Summ_Mass_Liquid ",Summ_Mass_Liquid,'\n')
    value = packet[10]|(packet[11]<<8)|(packet[12]<<16)|(packet[13]<<24)
    flo32 = struct.pack('I',value)
    Mass_FlowRate_Liquid = struct.unpack('f',flo32)
    print("Mass_FlowRate_Liquid ",Mass_FlowRate_Liquid,'\n')
    value = packet[14]|(packet[15]<<8)|(packet[16]<<16)|(packet[17]<<24)
    flo32 = struct.pack('I',value)
    Volume_FlowRate_Gas = struct.unpack('f',flo32)
    print("Volume_FlowRate_Gas ",Volume_FlowRate_Gas,'\n')

    value = packet[18]|(packet[19]<<8)|(packet[20]<<16)|(packet[21]<<24)
    flo32 = struct.pack('I',value)
    Mass_FlowRate_Oil = struct.unpack('f',flo32)
    print("Mass_FlowRate_Oil ",Mass_FlowRate_Oil,'\n')

    value = packet[22]|(packet[23]<<8)|(packet[24]<<16)|(packet[25]<<24)
    flo32 = struct.pack('I',value)
    Mass_FlowRate_Water = struct.unpack('f',flo32)
    print("Mass_FlowRate_Water ",Mass_FlowRate_Water,'\n')

    value = packet[26]|(packet[27]<<8)
    flo32 = value/10000
    print("Sr_Density_Liquid ",flo32,'\n')

    value = packet[28]|(packet[29]<<8)
    flo32 = value/100
    print("Sr_Temperature_Liquid ",flo32,'\n')

    value = packet[30]|(packet[31]<<8)
    flo32 = value/10000
    print("Sr_Wm_Water ",flo32,'\n')

    value = packet[32]|(packet[33]<<8)
    flo32 = value/10000
    print("Density_Oil_Save ",flo32,'\n')

    value = packet[34]|(packet[35]<<8)
    flo32 = value/10000
    print("Density_Water_Save ",flo32,'\n')

    value = packet[36]|(packet[37]<<8)
    flo32 = value/10000
    print("Density_Liquid_Save ",flo32,'\n')

    value = packet[38]|(packet[39]<<8)
    flo32 = value/100
    print("Pc_Gas ",flo32,'\n')


    value = packet[40]|(packet[41]<<8)
    print("CntTime ",value,'\n')

    value = packet[42]|(packet[43]<<8)
    print("Sync_Liquid ",value,'\n')

    value = packet[44]|(packet[45]<<8)
    print("OtvNumber ",value,'\n')

    value = packet[46]|(packet[47]<<8)|(packet[48]<<16)|(packet[49]<<24)
    flo32 = struct.pack('I',value)
    Summ_Volume_Gas = struct.unpack('f',flo32)
    print("Summ_Volume_Gas ",Summ_Volume_Gas,'\n')

    value = packet[50]|(packet[51]<<8)|(packet[52]<<16)|(packet[53]<<24)
    flo32 = struct.pack('I',value)
    Volume_FlowRate_Liquid = struct.unpack('f',flo32)
    print("Volume_FlowRate_Liquid ",Volume_FlowRate_Liquid,'\n')


  else:
    print('len packet mismatch\n',len(packet))


  return 1

