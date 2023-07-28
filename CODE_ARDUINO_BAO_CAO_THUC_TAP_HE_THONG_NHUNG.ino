#include <Servo.h>
#define IN1 4
#define IN2 3
#define IN3 6
#define IN4 5
#define CB 2 
Servo s1;
Servo s2;
//Servo s3;
int i=0;
int tam = 0;
int dulieu;
void test_servo()
{
  //for (i = 0; i <= 180; i++)
   // {
      s1.write(0);
      s2.write(0);
      //s3.write(i);
      delay(15);
   // }
}
void test_dc_run()
{
  digitalWrite(IN1, LOW);
  analogWrite(IN2, 200);
}
void test_dc_stop()
{
  digitalWrite(IN1, LOW);
  analogWrite(IN2, LOW);
}
void setup() 
{
  // put your setup code here, to run once:
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(CB,INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  s1.attach(9);
  s2.attach(10);
  Serial.begin(9600);
  //s3.attach(11);
  //Serial.begin(9600);
  
}

void loop() 
{
  int cbState = digitalRead(CB);
  if (cbState==1) // khong co cam bien thi gia tri 0
  {
      test_dc_run();
  }
  else
  {
    test_dc_stop();
   
    tam=1;
  
    s1.write(0);//servo ben phai
    s2.write(0);//servo ben trai
  }
 
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    dulieu=data.toInt();

  if(tam==1)
  {
  if (dulieu==3)
  {
    test_dc_stop();
    delay(3000);
    test_dc_run();
    s1.write(130);
    s2.write(0);
    delay(9000);
    s1.write(180);
    s2.write(0);
    tam=0;
  }
  else if (dulieu==5)
  {
    test_dc_stop();
    delay(3000);
    test_dc_run();
    s1.write(0);
    s2.write(45);
    delay(9000);
    s1.write(0);
    s2.write(0);
    tam=0;
  }
  }
  }
  
}
