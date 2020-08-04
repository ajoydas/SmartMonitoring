/*
 * To understand SIM808 application You are recommanded to read this small pdf gived below 
 * https://www.elecrow.com/download/SIM800%20Series_GNSS_Application%20Note%20V1.00.pdf
 */

//#include <SoftwareSerial.h>
#include<time.h>
#define DEBUG true
#define mySerial Serial3

#include <stdio.h>
#include<math.h>
#include <DFRobot_sim808.h>
//#define serialSIM808 Serial3

//Mobile phone number,need to change
#define PHONE_NUMBER  "012345678901"   
#define TRACKER_ID 12
 
DFRobot_SIM808 sim808;
char buffer[512];
char http_cmd[100];
char tracker[10];

// reverses a string 'str' of length 'len'
void reverse(char *str, int len)
{
    int i=0, j=len-1, temp;
    while (i<j)
    {
        temp = str[i];
        str[i] = str[j];
        str[j] = temp;
        i++; j--;
    }
}
 
 // Converts a given integer x to string str[].  d is the number
 // of digits required in output. If d is more than the number
 // of digits in x, then 0s are added at the beginning.
int intToStr(int x, char str[], int d)
{
    int i = 0;
    while (x)
    {
        str[i++] = (x%10) + '0';
        x = x/10;
    }
 
    // If number of digits required is more, then
    // add 0s at the beginning
    while (i < d)
        str[i++] = '0';
 
    reverse(str, i);
    str[i] = '\0';
    return i;
}
 
// Converts a floating point number to string.
void ftoa(float n, char *res, int afterpoint)
{
    // Extract integer part
    int ipart = (int)n;
 
    // Extract floating part
    float fpart = n - (float)ipart;
 
    // convert integer part to string
    int i = intToStr(ipart, res, 0);
 
    // check for display option after point
    if (afterpoint != 0)
    {
        res[i] = '.';  // add dot
 
        // Get the value of fraction part upto given no.
        // of points after dot. The third parameter is needed
        // to handle cases like 233.007
        fpart = fpart * pow(10, afterpoint);
 
        intToStr((int)fpart, res + i + 1, afterpoint);
    }
}


//SoftwareSerial mySerial(15, 14); // create gps sensor connection TX and RX accordingly - rx, tx
String state,timegps,lati,longi;
String latlongtab[5];

void initialize(){

    int i = 0;
    for(i=1;i<=4;i++){
      latlongtab[i]="";
    }
  
}

void validate_pass()
{
  //Serial.println("Validating password");
  int password = 234;
  char passw[20];
  itoa(password, passw, 10);
  itoa(TRACKER_ID, tracker,10);
  sprintf(http_cmd, "%s%s%s%s%s", "GET /api/validate/", tracker, "/", passw, " HTTP/1.0\r\n\r\n");

  Serial.println(http_cmd);
  //Serial.println(strlen(http_cmd));
  //*********** Attempt DHCP *******************
  while(!sim808.join(F("cmnet"))) {
      Serial.println("Sim808 join network error");
      delay(2000);
  }

  //************ Successful DHCP ****************
  //Serial.print("IP Address is ");
  //Serial.println(sim808.getIPAddress());

  //*********** Establish a TCP connection ************
  if(!sim808.connect(TCP,"do.ajoydas.com", 8080)) {
      Serial.println("Connect error");
  }else{
      Serial.println("Connect do.ajoydas.com success");
  }

  //*********** Send a GET request *****************
  Serial.println("waiting to fetch...");
  sim808.send(http_cmd, strlen(http_cmd));
  while (true) {
      int ret = sim808.recv(buffer, sizeof(buffer)-1);
      if (ret <= 0){
          Serial.println("fetch over...");
          break; 
      }
      buffer[ret] = '\0';
      Serial.print("Recv: ");
      Serial.print(ret);
      Serial.println(" bytes: ");
      Serial.println(buffer);
      //digitalWrite(38, HIGH);
      break;
  }

  //************* Close TCP or UDP connections **********
  sim808.close();

  //*** Disconnect wireless connection, Close Moving Scene *******
  sim808.disconnect();
  
}

void setup(){
  
  //mySerial.begin(9600); // connect serial
  Serial.begin(9600); // connect gps sensor
  delay(50);

  //********Initialize sim808 module*************
  while(!sim808.init()) { 
      delay(1000);
      Serial.print("Sim808 init error\r\n");
  }
  Serial.println("Sim808 init success");
  
  sendData("AT+CGNSPWR=1",1000,DEBUG); 
                                          /* ######## AT+CGNSPWR ######
                                              GNSS  = Global Navigation Satellite System
                                              0 - Turn off GNSS power supply
                                              1 - Turn on GNSS power supply
                                              return the current status of GNSS power supply,*/
  delay(50);
  sendData("AT+CGNSSEQ=RMC",1000,DEBUG);  
                                          /*  #####  AT+CGNSSEQ  #####
                                              Get the current setting of last sentence parsed,
                                              GGA - Time, position, and fix type data
                                              GSA - GNSS receiver operating mode, satellites used and DOP values.
                                              GSV - Number of satellies in view, satellite ID numbers, elevation, azimuth & SNR values
                                              RMC - Time, date, position, course and speed data */
                                              
  delay(150);
  //*********Validate Password***************
  //validate_pass(); 
  
}

void sendGPS()
{
  initialize();
  sendTabData("AT+CGNSINF",1000,DEBUG);
  
  
  if(state != 0){
  
    Serial.println("State    : "+state);
    Serial.println("Time     : "+timegps);
    Serial.println("latitude : "+lati);
    Serial.println("longitude: "+longi);
    initialize();
  
  }else{
 
    Serial.println("Gps initializing");
  }
}
void loop(){
  sendGPS();
  
}

void sendTabData(String command,const int timeout,boolean debug){

  mySerial.println(command);
  long int time = millis();
  int i =0;

  while((time+timeout)>millis()){

      while( mySerial.available() ){
        
        char c= mySerial.read();
        if( c!= ',' ){
          latlongtab[i]+=c;
          delay(100);
        }else{
          i++;
        }
        if( i ==5 ){
          delay(100);
          goto exitL;
        }
        
      }
  }exitL:
  if(debug){
    state = latlongtab[1];
    timegps = latlongtab[2];
    lati = latlongtab[3];
    longi = latlongtab[4];
  }


}
  

String sendData(String command,const int timeout,boolean debug){

  String response = "";
  mySerial.println(command);
  long int time = millis();
  int i =0;

  while((time+timeout)>millis()){

      while( mySerial.available() ){
        char c= mySerial.read();
        response+=c;
      }
  }
  Serial.println("Response:");
  if(debug){
    Serial.println(response);
  }
  return response;


}

