# dwm version
VERSION = 6.3

# Customize below to fit your system

# paths
PREFIX = /usr/local
MANPREFIX = ${PREFIX}/share/man

X11INC = /usr/include/X11
X11LIB = /usr/lib/X11

# Xinerama, comment if you don't want it
XINERAMALIBS  = -lXinerama
XINERAMAFLAGS = -DXINERAMA

# freetype
FREETYPELIBS = -lfontconfig -lXft
FREETYPEINC = /usr/include/freetype2
# OpenBSD (uncomment)
#FREETYPEINC = ${X11INC}/freetype2

# includes and libs
INCS = -I${X11INC} -I${FREETYPEINC}
LIBS = -L${X11LIB} -lX11 ${XINERAMALIBS} ${FREETYPELIBS} -lXrender

# flags
CPPFLAGS = -D_DEFAULT_SOURCE -D_BSD_SOURCE -D_POSIX_C_SOURCE=200809L -DVERSION=\"${VERSION}\"  ${XINERAMAFLAGS}
# CPPFLAGS += -D_DEFAULT_SOURCE 

CXXFLAGS +=  -std=c++14
CXXFLAGS += -pedantic
CXXFLAGS += -Wall
CXXFLAGS += -Wno-deprecated-declarations
# CXXFLAGS += -Wno-unused-parameter
CXXFLAGS += -g -O3 ${INCS} ${CPPFLAGS}

# LDFLAGS  = ${LIBS}
LDFLAGS  = -s ${LIBS}


# compiler and linker
# CC = cc
CXX = g++
