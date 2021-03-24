char action;

void setup() {
Serial.begin(9600);
pinMode(13,OUTPUT);
}

void loop() {
if(Serial.available())
  action=Serial.read();

if(action=='1')
  digitalWrite(13,HIGH);
if(action=='0')
  digitalWrite(13,LOW);
}
