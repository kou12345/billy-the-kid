#include <Servo.h>

String receivedData;
Servo myservo;  // サーボモーターのインスタンス変数を生成

void setup() {
  Serial.begin(9600);  // シリアル通信速度を9600bpsに設定
  pinMode(8, OUTPUT);
  pinMode(6, OUTPUT);
  myservo.attach(9);  // 9番PINをサーボモーターの制御に使用
}

void loop() {

  if (Serial.available() > 0) {
    char receivedChar = Serial.read();
    Serial.println(receivedChar);

    if (receivedChar == '\n') {
      receivedData.trim();

      Serial.print("Received: ");
      Serial.println(receivedData);

      int receivedValue = receivedData.toInt();
      Serial.println(receivedValue);

      if (receivedValue) {
        for (int i = 0; i < 5; i++) {
          digitalWrite(6, HIGH);
          delay(500);
          digitalWrite(6, LOW);
          delay(250);
        }
      }

      if (receivedValue == 123) {
        Serial.println("true");
        for (int i = 0; i < 5; i++) {
          digitalWrite(8, HIGH);
          delay(500);
          digitalWrite(8, LOW);
          delay(250);
        }

        // サーボモータを回転させる
        myservo.write(0);  // 0度の位置にサーボを移動
        delay(1000);
        myservo.write(90);  // 90度の位置にサーボを移動
        delay(1000);
        myservo.write(180);  // 180度の位置にサーボを移動
        delay(1000);
      }

      receivedData = "";
    } else {
      receivedData += receivedChar;
    }
  }
}