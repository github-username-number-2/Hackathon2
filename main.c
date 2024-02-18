/*
PD0 motor signal
PD1 left aileron signal
PD2 right aileron signal
PD3 elevators
PD4 rudder
PD5 bay doors
*/

#define F_CPU 16000000

#include <avr/sfr_defs.h>
#define __DELAY_BACKWARD_COMPATIBLE__
#include <util/delay.h>
#include <avr/io.h>
#include <avr/interrupt.h>

struct nrfPacket {
	uint8_t motor;
	uint8_t rotationZ; // ailerons
	uint8_t rotationX; // elevators
	uint8_t rudder;
	uint8_t bayDoors;
};

// 0-255
uint8_t pwmDutys[5] = {0, 64, 128, 172, 255};

int main(void) {
  DDRB = _BV(PB5);
	DDRD = 0b11111000;
	
	// arm esc
	uint8_t i = 255;
  while(i--) {
    PORTD = _BV(PD0);
		_delay_ms(1);
		PORTD = _BV(PD0);
		_delay_ms(19);
  }
	
	// configure timer  
  TCNT1 = 65223; // 16000000/1024/(65535-65223) for 50.0801282Hz
  TCCR1A = 0x00;
	TCCR1B = _BV(CS10) | _BV(CS12);
	TIMSK1 = _BV(1TOIE1);
	
	sei();

  while (1) {
    //
  }
}

ISR (TIMER1_OVF_vect) {
  TCNT1 = 65223;

  PORTD |= 0b11111000;

  DDRB ^= _BV(PB5);

  uint16_t currentDelay = 0;
  for (uint8_t i = 3; i < 8; i++) {
    /*uint16_t delay = 2000 / pwmDutys[i] + 500 - currentDelay;
    currentDelay += delay;

    while (delay--) continue;*/
    _delay_ms(.5);
    
    PORTD &= ~_BV(i);
  }
}