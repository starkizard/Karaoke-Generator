import wave
import array


def combine(path1,path2,path3,path4):
    w1 = wave.open(path1)
    w2 = wave.open(path2)
    w3 = wave.open(path3)
    w4 = wave.open(path4)
    

    #get samples formatted as a string.
    samples1 = w1.readframes(w1.getnframes())
    samples2 = w2.readframes(w2.getnframes())
    samples3 = w3.readframes(w3.getnframes())
    samples4 = w4.readframes(w4.getnframes())


    print("samples done ")

    #takes every 2 bytes and groups them together as 1 sample. ("123456" -> ["12", "34", "56"])
    samples1 = [samples1[i:i+2] for i in range(0, len(samples1), 2)]
    samples2 = [samples2[i:i+2] for i in range(0, len(samples2), 2)]
    samples3 = [samples3[i:i+2] for i in range(0, len(samples3), 2)]
    samples4 = [samples4[i:i+2] for i in range(0, len(samples4), 2)]
    
    print("Grouping done")
    #convert samples from strings to ints
    
    def bin_to_int(bin):
        as_int = 0
        for char in bin[::-1]: #iterate over each char in reverse (because little-endian)
            #get the integer value of char and assign to the lowest byte of as_int, shifting the rest up
            as_int <<= 8
            as_int += char
        return as_int

    samples1 = [bin_to_int(s) for s in samples1] #['\x04\x08'] -> [0x0804]
    samples2 = [bin_to_int(s) for s in samples2]
    samples3 = [bin_to_int(s) for s in samples3] 
    samples4 = [bin_to_int(s) for s in samples4]

    print("binary to integer done")

    #average the samples:
    samples_avg = [(s1+s2+s3+s4) for (s1, s2 , s3 , s4) in zip(samples1, samples2 , samples3, samples4)]

    print("averaging done")

    samples_array = array.array('i')
    samples_array.fromlist(samples_avg)

    wave_out = wave.open ("./output/out.wav", "wb")

    print("Output file loaded")

    wave_out.setnchannels(1)
    wave_out.setsampwidth(2)
    wave_out.setframerate(w1.getframerate()*4) 
    wave_out.writeframes(samples_array)

    print("File written ")

def main():
    
    s = input( "Enter song name ")

    print("Generate Karoke for: ")
    print("1. Vocals")
    print("2. Piano ")
    print("3. Drums ")
    print("4. Bass ")
    print("5. Other accompaniment")

    c=int(input("Enter the choice number:\t"))
    total=["vocals","piano","drums","bass","other"]
    
    total.pop(c-1)
    total = ["./output/"+s+"/"+x+".wav" for x in total] 

    combine(*total)

    print("Output file made : ./output/out.wav ")


main()