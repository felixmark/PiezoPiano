// MidiPlayer

#define F_TIMER				65536/2
#define TCA_LIMIT			((F_CPU/F_TIMER)+1)

#define DELAYVAL 400      // Time (in milliseconds) to pause between pixels

#define OFFSET 8          // Tuned by pianist

int noteDuration = 100;   // Note dauration for the test

int pos_piezo[] = {9, 8, 7, 6, 5, 4, 1, 0};       // Digital pin location for the piezos starting from left to right V1.3 +

class Note {
  public:
    int frequency;
    int duration;
    Note(int frequency, int duration) {
      this->frequency = frequency;
      this->duration = duration;
    }
};

Note song[] = {
  Note(440,1000)
};

void setup() {
  // ----------------- INIT GPIO -----------------
  GPIO_Init();

  // ----------------- ACTIVATE SERIAL -----------------
  Serial1.begin(9600);
}

void loop() {
    for(int i = 0; i < 1; i++) {
        tone(pos_piezo[i], song[i].frequency, song[i].duration);
        delay(song[i].duration);
        noTone(pos_piezo[i]);
    }
}

void GPIO_Init()
{
  // Piezos
  pinMode(pos_piezo[0], OUTPUT);
  pinMode(pos_piezo[1], OUTPUT);
  pinMode(pos_piezo[2], OUTPUT);
  pinMode(pos_piezo[3], OUTPUT);
  pinMode(pos_piezo[4], OUTPUT);
  pinMode(pos_piezo[5], OUTPUT);
  pinMode(pos_piezo[6], OUTPUT);
  pinMode(pos_piezo[7], OUTPUT);

  digitalWrite(pos_piezo[0], LOW);
  digitalWrite(pos_piezo[1], LOW);
  digitalWrite(pos_piezo[2], LOW);
  digitalWrite(pos_piezo[3], LOW);
  digitalWrite(pos_piezo[4], LOW);
  digitalWrite(pos_piezo[5], LOW);
  digitalWrite(pos_piezo[6], LOW);
  digitalWrite(pos_piezo[7], LOW);
}
