#include <iostream>
#include <attoDRYLib.h>
#include <ctime>
#include <stdlib.h>     /* atof */




/*
The DLL reuires the following to be installed:
-Labview 2015 32bit runtime engine
-VISA run time engine

Ensure you include and link extcode.h and it's includes. It can be found here C:\Program Files (x86)\National Instruments\LabVIEW 2012\cintools
 or, you can use the files included with the DLL.

 If you are uing mingw compiler, you may need to add the lines

 #elif defined(__GNUC__)
        #define Compiler    kGCC
 just before where you get the "#error "We don't know the Compiler"" in platdefines.h

 and

 #elif Compiler == kGCC
        #define ProcessorType	kX86

 just before where you get the "#error "We don't know the ProcessorType architecture"" in platdefines.h
*/



// a function used for a delay
inline void mySleep(clock_t sec) // clock_t is a like typedef unsigned int clock_t. Use clock_t instead of integer in this context
{
     clock_t start_time = clock();
     clock_t end_time = sec * 1000 + start_time;
     while(clock() != end_time);
}

using namespace std;
std::string myPort; // string for storing the COM Port
float userTemp; // a variable for storing user temperature
std::string desiredStr; //desired user temperature, as a string
std::string path; //path for logging data
uint8_t err;    // used for the attoDRY error code
float P_gain;   // a variable for storing proportional gain
int running;  // a boolean for checking if the attoDRY is initialised
int HeValve;

const int32_t errorMsgLength = 500; // maximum length of the array for storing the error message.
                                    //When dealing with strings, you must give labview the maximum length
char errorMsg[errorMsgLength];      // array for storing error message

// disconnects and closes the server
int32_t AttoDRY_Interface_closeServer(){
    int32_t error = AttoDRY_Interface_Disconnect();
    cout << "Disconnected"  << endl;
    error = AttoDRY_Interface_end();
   cout << "Ended"  << endl;
    return error;
}

int32_t e;

int main()
{

    std::cout << "Enter the COM port (e.g. COM6)" << std::endl;

    std::getline(std::cin,myPort);

    std::cout << "Enter the file for logging e.g. E:\\myLog.txt" << std::endl;

    std::getline(std::cin,path);

    // start he attoDRY interface server. The user interface queue is not used in the DLL, so put NULL here.
    e = AttoDRY_Interface_begin(AttoDRY_Interface_Device_attoDRY800);
    if (e){
        AttoDRY_Interface_end();
        return e;
    }

cout << "Begin" << endl;

    // Connect to your com port
    e = AttoDRY_Interface_Connect(const_cast<char *>(myPort.c_str()));
    // check to see if there was an error
     if (e){
         // there was an error. End the program
        return e;
    }
     cout << "Connected" << endl;

//     wait for the attoDRY to initialise
   while (!running){
        e = AttoDRY_Interface_isDeviceInitialised(&running);
        if (e){
           AttoDRY_Interface_closeServer();
            return e;
        }
    }
     cout << "running"  << endl;

    std::cout << "Enter desired user temperature (4 to 300K)" << std::endl;
    std::getline(std::cin,desiredStr);

    // set the user temperature. Convert it from a string to a float
     e = AttoDRY_Interface_setUserTemperature(atof(desiredStr.c_str()));
     if (e){
         AttoDRY_Interface_closeServer();
        return e;
    }

    // get the user temperature. Notice that the value is not what you set, yet.
    //It takes a couple of seconds for the command to be sent to the attoDRY
    //and for the attoDRY to send an updated status message
    e = AttoDRY_Interface_getUserTemperature(&userTemp);
     if (e){
         AttoDRY_Interface_closeServer();
        return e;
    }
    cout << "GetUserTemperature " << userTemp << endl;

    e = AttoDRY_Interface_toggleSampleSpace800Valve();
    if (e){
         AttoDRY_Interface_closeServer();
        return e;
    }

    mySleep(1);

        e = AttoDRY_Interface_toggleSampleSpace800Valve();
    if (e){
         AttoDRY_Interface_closeServer();
        return e;
    }

    mySleep(1);

    // get the proportional gain
    e = AttoDRY_Interface_getProportionalGain(&P_gain);
    if (e){
        AttoDRY_Interface_closeServer();
        return e;
    }
    cout << "GetProportionalGain " << P_gain << endl;



    // start logging data
    e = AttoDRY_Interface_startLogging(const_cast<char *>(path.c_str()), Enum__1Second,int(0));
	if (e){
	    AttoDRY_Interface_closeServer();
        return e;

	}
    // check to see if the attoDRY has an error
    e = AttoDRY_Interface_getAttodryErrorStatus(&err);
    if (e){
        AttoDRY_Interface_closeServer();
        return e;
    }
    cout << "GetAttodryErrorStatus " << (int)(err) << endl;

    // wait for 10 seconds so that there is spome data in the log file
	mySleep(10);

    // get the user temperature now. It should be updated with the temperature you set
	e = AttoDRY_Interface_getUserTemperature(&userTemp);
     if (e){
         AttoDRY_Interface_closeServer();
        return e;
    }
    cout << "GetUserTemperature " << userTemp << endl;

    // stop logging
	e = AttoDRY_Interface_stopLogging();
	if (e){
	    AttoDRY_Interface_closeServer();
        return e;
    }

    // check again to see if there is an error on the AttoDRY
    e = AttoDRY_Interface_getAttodryErrorMessage(errorMsg, errorMsgLength);
    if (e){
        AttoDRY_Interface_closeServer();
        return e;
    }
    cout << "GetAttodryErrorMessage " << errorMsg << endl;

    // finished with the attoDRY. Disconnect and close the server
    AttoDRY_Interface_closeServer();
    if (e){
        return e;
    }



    // No errors occured
    return 0;
}
