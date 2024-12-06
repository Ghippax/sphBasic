CC = g++
LD = g++

TARGET = run

LIBS = -lhdf5

CFLAGS = -I/home/libs/hdf5/include
LFLAGS = -L/home/libs/hdf5/lib

OBJS = obj/main.o

all: $(TARGET)

$(TARGET): $(OBJS)
	$(LD) $(LFLAGS) $(OBJS) $(LIBS) -o $(TARGET)

obj/main.o: src/main.cc
	mkdir -p obj
	$(CC) $(CFLAGS) -c src/main.cc -o obj/main.o

clean:
	rm -f $(OBJS)
	rm -f $(TARGET)
	rm -f $(TARGET).exe
	rmdir obj
