// Reference to original script which was modified
// Name: timelapse_recorder.ino
//Author: Ryotaro Okamoto
//Started: 2023/1/30
//Last Modified: 2025/07/15
//Purpose: To perform time-lapse audio recordings using Sony Spresense
//Reference: https://doi.org/10.1111/2041-210X.14474

//


#include <LowPower.h>
#include <RTC.h>
#include <SDHCI.h>
#include <Audio.h>
#include <Watchdog.h>

#define BAUDRATE 115200
#define SERIAL2_BAUD 115200
#define MY_TIMEZONE_IN_SECONDS (0 * 60 * 60) // GMT

// Schedule settings: From 09:00 to 18:00 at minutes 0, 15, 30, and 45
typedef struct {
  int start_h;
  int end_h;
  int m[100];
} schedule;

schedule s = {09, 18, {0,15, 30, 45}};

static const int32_t codec = AS_CODECTYPE_WAV;
static const int32_t recording_time = 60;
static const int32_t gain = 210;
static const bool is_digital = false;
static const int32_t channel = AS_CHANNEL_STEREO;
static const int32_t sr = AS_SAMPLINGRATE_48000;
static const uint8_t recoding_bit_length = 16;

String out_dir = "AUDIO";

const char* boot_cause_strings[] = {
  "Power On Reset with Power Supplied", "System WDT expired or Self Reboot",
  "Chip WDT expired", "WKUPL signal detected in deep sleep",
  "WKUPS signal detected in deep sleep", "RTC Alarm expired in deep sleep",
  "USB Connected in deep sleep", "Others in deep sleep",
  "SCU Interrupt detected in cold sleep", "RTC Alarm0 expired in cold sleep",
  "RTC Alarm1 expired in cold sleep", "RTC Alarm2 expired in cold sleep",
  "RTC Alarm Error occurred in cold sleep", "Unknown(13)", "Unknown(14)", "Unknown(15)",
  "GPIO detected in cold sleep", "GPIO detected in cold sleep", "GPIO detected in cold sleep",
  "GPIO detected in cold sleep", "GPIO detected in cold sleep", "GPIO detected in cold sleep",
  "GPIO detected in cold sleep", "GPIO detected in cold sleep", "GPIO detected in cold sleep",
  "GPIO detected in cold sleep", "GPIO detected in cold sleep", "GPIO detected in cold sleep",
  "SEN_INT signal detected in cold sleep", "PMIC signal detected in cold sleep",
  "USB Disconnected in cold sleep", "USB Connected in cold sleep", "Power On Reset"
};

void printBootCause(bootcause_e bc) {
  Serial.println("--------------------------------------------------");
  Serial.print("Boot Cause: ");
  Serial.println(boot_cause_strings[bc]);
  Serial.println("--------------------------------------------------");
}

String printClock(RtcTime &rtc) {
  char buf[20];
  sprintf(buf, "%04d%02d%02d_%02d%02d", rtc.year(), rtc.month(), rtc.day(), rtc.hour(), rtc.minute());
  return String(buf);
}

void setLowPower() {
  bootcause_e bc = LowPower.bootCause();
  Serial.println((bc == POR_SUPPLY || bc == POR_NORMAL) ? "Beemic starting!" : "Woke up from deep sleep");
  printBootCause(bc);
}

void findMinute(schedule s, int *next_minute, int *next_hour, RtcTime rtc) {
  bool found = false;
  for (int i = 0; i < sizeof(s.m) / sizeof(int); i++) {
    if (s.m[i] > rtc.minute()) {
      *next_minute = s.m[i];
      *next_hour = rtc.hour();
      found = true;
      break;
    }
  }
  if (!found) {
    *next_minute = s.m[0];
    *next_hour = rtc.hour() + 1;
  }
}

int getNextAlarm(schedule s, RtcTime rtc) {
  int next_hour, next_minute = s.m[0];
  int next_date = rtc.day();

  if ((rtc.hour() >= s.start_h) && (rtc.hour() <= s.end_h)) {
    findMinute(s, &next_minute, &next_hour, rtc);
  } else if (rtc.hour() < s.start_h) {
    next_hour = s.start_h;
  } else {
    next_hour = s.start_h;
    next_date++;
  }

  RtcTime rtc_to_alarm(rtc.year(), rtc.month(), next_date, next_hour, next_minute, 0);
  Serial.println("The next boot time is " + printClock(rtc_to_alarm));
  int sleep_sec = rtc_to_alarm.unixtime() - rtc.unixtime();
  return max(sleep_sec, 0);
}

// Audio setup
int32_t recoding_size;
int buff_size;
String ext;
SDClass theSD;
AudioClass *theAudio;
File myFile;
bool ErrEnd = false;
const int wd_time = 20000;

static void audio_attention_cb(const ErrorAttentionParam *atprm) {
  if (atprm->error_code >= AS_ATTENTION_CODE_WARNING) ErrEnd = true;
}

void initAudio() {
  Serial.begin(BAUDRATE);
  Serial2.begin(SERIAL2_BAUD);  // For communication to NodeMCU

  while (!theSD.begin()) Serial.println("Insert SD card.");
  if (!theSD.exists(out_dir)) theSD.mkdir(out_dir);

  if (codec == AS_CODECTYPE_WAV) {
    recoding_size = sr * channel * recoding_bit_length / 8 * recording_time;
    buff_size = (sr == AS_SAMPLINGRATE_192000) ? 320000 : 160000;
    ext = ".wav";
  }

  theAudio = AudioClass::getInstance();
  theAudio->begin(audio_attention_cb);
  if (sr == AS_SAMPLINGRATE_192000)
    theAudio->setRenderingClockMode(AS_CLKMODE_HIRES);

  theAudio->setRecorderMode(AS_SETRECDR_STS_INPUTDEVICE_MIC, gain, buff_size, is_digital);
  theAudio->initRecorder(codec, "/mnt/sd0/BIN", sr, channel);
}

void exit_recording() {
  theAudio->closeOutputFile(myFile);
  myFile.close();
  theAudio->setReadyMode();
  theAudio->end();
  Serial.println("Recording error. Exiting...");
}

bool rec(String file_name) {
  myFile = theSD.open(file_name, FILE_WRITE);
  if (!myFile) return false;

  if (codec == AS_CODECTYPE_WAV) theAudio->writeWavHeader(myFile);
  theAudio->startRecorder();
  Serial.println("Recording Start!");

  err_t err;
  while (theAudio->getRecordingSize() < recoding_size) {
    err = theAudio->readFrames(myFile);
    if (err != AUDIOLIB_ECODE_OK || ErrEnd) {
      theAudio->stopRecorder();
      exit_recording();
      return false;
    }
    Watchdog.kick();
  }

  theAudio->stopRecorder();
  sleep(1);
  theAudio->closeOutputFile(myFile);
  myFile.close();
  Serial.println("Recording finished!");
  Serial2.println("start_show");
  Serial.println("Sent 'start_show' to NodeMCU");

  return true;
}

// Main
bool rec_ok = true;
String file_name;
int sleep_sec;
RtcTime now;

void setup() {
  Serial.begin(115200);
  while (!Serial);
  Serial.println("Starting!");

  RTC.begin();

  bootcause_e bc = LowPower.bootCause();
  if (bc == POR_SUPPLY || bc == POR_NORMAL) {
    Serial.println("First power-on: setting RTC time manually.");
    RtcTime myTime(2025, 7, 17, 13, 46, 0);
    RTC.setTime(myTime);
  } else {
    Serial.println("Woke up from deep sleep.");
  }

  printBootCause(bc);
  Watchdog.begin();
  initAudio();
  Watchdog.start(wd_time);
}

void loop() {
  now = RTC.getTime();
  file_name = out_dir + "/" + printClock(now) + ext;
  rec_ok = rec(file_name);
  if (!rec_ok) {
    while (true) {
      delay(1000);
      Serial.println("Watchdog remains: " + String(Watchdog.timeleft() / 1000) + " sec");
    }
  }
  Watchdog.kick();
  now = RTC.getTime();
  sleep_sec = getNextAlarm(s, now);
  if (sleep_sec > 0) LowPower.deepSleep(sleep_sec);
}
