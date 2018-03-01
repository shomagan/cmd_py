def main():
  have_serial = 1
#  devpy.color_traceback()
#  log = devpy.autolog() # log is a regular stdlib logger object
#  log.info('Yes')
  try:
    ser = serial.Serial('COM8')
    ser.baudrate = 9600;
    print (ser.name)          # check which port was really used
    sys.stderr.write('--- Miniterm on %s: %d,%s,%s,%s ---\n' % (
      ser.portstr,
      ser.baudrate,
      ser.bytesize,
      ser.parity,
      ser.stopbits,
    ))
  except serial.SerialException as e:
    have_serial = 0
    print("could not open port \n")
  request_cc = [0x00,0x02]
  while 1:
#    if msvcrt.kbhit():
    q = msvcrt.getch()
    print(ord(q))
    if ord(q) == 113:#q
      s.close()
      sys.exit(1)
    elif ord(q)==109:#m

      crc = crc16(mdb_rtu,len(mdb_rtu))
      mdb_rtu.append(crc&0xFF)
      mdb_rtu.append((crc>>8)&0xFF)
      print (mdb_rtu)

      if have_serial:
        ser.reset_input_buffer()
        ser.write(mdb_rtu)
        if arc_parse:
          ser.timeout = 0.4
          receive_buff = ser.read(59)
          buff_temp = [receive_buff[i] for i in range(3,57)]
#          arc_parse(buff_temp)

  
if __name__ == "__main__":
    main()
