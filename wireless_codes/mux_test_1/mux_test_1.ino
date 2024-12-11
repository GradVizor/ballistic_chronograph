#define S0  0
#define S1  1
#define S2  2 
#define S3  3
#define Signal 4

void setup() {
  Serial.begin(9600);
  pinMode(S0,OUTPUT);
  pinMode(S1,OUTPUT);
  pinMode(S2,OUTPUT);
  pinMode(S3,OUTPUT);
  pinMode(Signal,OUTPUT);

}

void loop() {
  int Sel0 = digitalRead(S0);
  int Sel1 = digitalRead(S1);
  int Sel2 = digitalRead(S2);
  int Sel3 = digitalRead(S3);
  int Signal_ = digitalRead(Signal);

  Serial.print(Sel3);
  Serial.print(Sel2);
  Serial.print(Sel1);
  Serial.println(Sel0);
  Serial.print("Signal:- ");
  Serial.println(Signal_);
  Serial.println("_____________________");
  delay(100);
  
}
