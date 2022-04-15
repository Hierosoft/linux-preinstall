# Free Casual Games for Linux

## Descriptions

(*) = From Mainstream Repos
(such as arch, via Antergos graphical package manager search for "game" [more results than justing using the Game category])

* (*) abuse
* (*) digger
* (*) dwarffortress
* (*) dynablaster-revenge
* (*) tomatoes "I Have No Tomatoes"
* (*) barrage
* (*) blobwars "Blob Wars: Metal Blob Solid"
* (*) btanks
* (*) clickety
* (*) glhack
* (*) gnujump
* (*) instead-launcher
* (*) kblocks
* (*) kbreakout
* (*) killbots
* (*) KSpaceDuel
* (*) megaglest 
* (*) naev
* (*) performous
* (*) pingus
* (*) spring (and spring-1944 game for spring)
* (*) supertux
* (*) teeworlds
* (*) wesnoth
* (*) widelands
* (*) xpacman
* (*) xpacman2
* (*) xbill
* (*) xmoto
* (*) zazz 

### Too low-fi
* (*) lincity-ng
* (*) slimevolley


## Not looked over yet
e and higher letters for search "game" in AUR

## Wouldn't install
* adanaxis-gpl "shooter game in four spacial dimentions"
* adonthell-wastesedge
* after-school "handpainted on paper, using pencil and watercolors"
* bitfighter "team-based outer-space multi-player combat game"
	tried to download a zip file from google code (Google Code is discontinued)
* caveexpress (many SDL typedef redefinitions)
* castles-in-the-sky "package filename is not valid"
* droidquest "package filename is not valid"

## Not tried
bombermaaan (multiplayer bomberman clone)
doukutsu (japanese version of Cave Story nonfree)
dreamweb (dystopian city adventure game)

## Descriptions
* adom - plot-driven roguelike
* atari-combat
* avanor
* balazarbrothers
* ballerburg
* blackvoxel

## Commercial Games
This is only a list of commercial games that aren't marked as such in AUR
(packages ending in -hib aren't included in this list).
(hib) = Requires installation via Steam? (hib protocol--Humble Indie Bundle)
* albion-online*
* (hib) dontstarve

## I did not review games I consider special interest games
* board games
	* (*) KSirk is a world-domination strategy game
	* (*) konquest
	* (*) xmahjongg
* (purely) puzzle games
	* (*) fillets-ng
	* (*) freedroid
	* (*) gweled
* card games
	* (*) frtg "Race for the Galaxy"
* sports games
	* (*) golf
* (purely) physics games
	* (*) caph "Sandbox game based on physics"
	* (*) kollision


## details of errors:
### caveexpress
```
In file included from /usr/include/SDL2/SDL_mixer.h:27:0,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_stdinc.h:141:17: error: redeclaration of ‘SDL_FALSE’
     SDL_FALSE = 0,
                 ^
In file included from src/libs/SDL/include/SDL_main.h:25:0,
                 from src/libs/SDL/include/SDL.h:32,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_stdinc.h:128:5: note: previous declaration ‘SDL_bool SDL_FALSE’
     SDL_FALSE = 0,
     ^~~~~~~~~
In file included from /usr/include/SDL2/SDL_mixer.h:27:0,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_stdinc.h:142:16: error: redeclaration of ‘SDL_TRUE’
     SDL_TRUE = 1
                ^
In file included from src/libs/SDL/include/SDL_main.h:25:0,
                 from src/libs/SDL/include/SDL.h:32,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_stdinc.h:129:5: note: previous declaration ‘SDL_bool SDL_TRUE’
     SDL_TRUE = 1
     ^~~~~~~~
In file included from /usr/include/SDL2/SDL_mixer.h:27:0,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_stdinc.h:143:3: error: conflicting declaration ‘typedef enum SDL_bool SDL_bool’
 } SDL_bool;
   ^~~~~~~~
In file included from src/libs/SDL/include/SDL_main.h:25:0,
                 from src/libs/SDL/include/SDL.h:32,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_stdinc.h:130:3: note: previous declaration as ‘typedef enum SDL_bool SDL_bool’
 } SDL_bool;
   ^~~~~~~~
In file included from /usr/include/SDL2/SDL_mixer.h:27:0,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_stdinc.h:301:5: error: redeclaration of ‘DUMMY_ENUM_VALUE’
     DUMMY_ENUM_VALUE
     ^~~~~~~~~~~~~~~~
In file included from src/libs/SDL/include/SDL_main.h:25:0,
                 from src/libs/SDL/include/SDL.h:32,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_stdinc.h:279:5: note: previous declaration ‘SDL_DUMMY_ENUM DUMMY_ENUM_VALUE’
     DUMMY_ENUM_VALUE
     ^~~~~~~~~~~~~~~~
In file included from /usr/include/SDL2/SDL_mixer.h:27:0,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_stdinc.h:302:3: error: conflicting declaration ‘typedef enum SDL_DUMMY_ENUM SDL_DUMMY_ENUM’
 } SDL_DUMMY_ENUM;
   ^~~~~~~~~~~~~~
In file included from src/libs/SDL/include/SDL_main.h:25:0,
                 from src/libs/SDL/include/SDL.h:32,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_stdinc.h:280:3: note: previous declaration as ‘typedef enum SDL_DUMMY_ENUM SDL_DUMMY_ENUM’
 } SDL_DUMMY_ENUM;
   ^~~~~~~~~~~~~~
In file included from /usr/include/SDL2/SDL_mixer.h:27:0,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_stdinc.h: In function ‘void SDL_memset4(void*, Uint32, size_t)’:
/usr/include/SDL2/SDL_stdinc.h:373:23: error: redefinition of ‘void SDL_memset4(void*, Uint32, size_t)’
 SDL_FORCE_INLINE void SDL_memset4(void *dst, Uint32 val, size_t dwords)
                       ^~~~~~~~~~~
In file included from src/libs/SDL/include/SDL_main.h:25:0,
                 from src/libs/SDL/include/SDL.h:32,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_stdinc.h:351:23: note: ‘void SDL_memset4(void*, Uint32, size_t)’ previously defined here
 SDL_FORCE_INLINE void SDL_memset4(void *dst, Uint32 val, size_t dwords)
                       ^~~~~~~~~~~
In file included from /usr/include/SDL2/SDL_mixer.h:27:0,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_stdinc.h: In function ‘void* SDL_memcpy4(void*, const void*, size_t)’:
/usr/include/SDL2/SDL_stdinc.h:530:24: error: redefinition of ‘void* SDL_memcpy4(void*, const void*, size_t)’
 SDL_FORCE_INLINE void *SDL_memcpy4(SDL_OUT_BYTECAP(dwords*4) void *dst, SDL_IN_BYTECAP(dwords*4) const void *src, size_t dwords)
                        ^~~~~~~~~~~
In file included from src/libs/SDL/include/SDL_main.h:25:0,
                 from src/libs/SDL/include/SDL.h:32,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_stdinc.h:382:24: note: ‘void* SDL_memcpy4(void*, const void*, size_t)’ previously defined here
 SDL_FORCE_INLINE void *SDL_memcpy4(SDL_OUT_BYTECAP(dwords*4) void *dst, SDL_IN_BYTECAP(dwords*4) const void *src, size_t dwords)
                        ^~~~~~~~~~~
In file included from /usr/include/SDL2/SDL_rwops.h:33:0,
                 from /usr/include/SDL2/SDL_mixer.h:28,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_error.h: At global scope:
/usr/include/SDL2/SDL_error.h:57:5: error: redeclaration of ‘SDL_ENOMEM’
     SDL_ENOMEM,
     ^~~~~~~~~~
In file included from src/libs/SDL/include/SDL_audio.h:32:0,
                 from src/libs/SDL/include/SDL.h:36,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_error.h:57:5: note: previous declaration ‘SDL_errorcode SDL_ENOMEM’
     SDL_ENOMEM,
     ^~~~~~~~~~
In file included from /usr/include/SDL2/SDL_rwops.h:33:0,
                 from /usr/include/SDL2/SDL_mixer.h:28,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_error.h:58:5: error: redeclaration of ‘SDL_EFREAD’
     SDL_EFREAD,
     ^~~~~~~~~~
In file included from src/libs/SDL/include/SDL_audio.h:32:0,
                 from src/libs/SDL/include/SDL.h:36,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_error.h:58:5: note: previous declaration ‘SDL_errorcode SDL_EFREAD’
     SDL_EFREAD,
     ^~~~~~~~~~
In file included from /usr/include/SDL2/SDL_rwops.h:33:0,
                 from /usr/include/SDL2/SDL_mixer.h:28,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_error.h:59:5: error: redeclaration of ‘SDL_EFWRITE’
     SDL_EFWRITE,
     ^~~~~~~~~~~
In file included from src/libs/SDL/include/SDL_audio.h:32:0,
                 from src/libs/SDL/include/SDL.h:36,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_error.h:59:5: note: previous declaration ‘SDL_errorcode SDL_EFWRITE’
     SDL_EFWRITE,
     ^~~~~~~~~~~
In file included from /usr/include/SDL2/SDL_rwops.h:33:0,
                 from /usr/include/SDL2/SDL_mixer.h:28,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_error.h:60:5: error: redeclaration of ‘SDL_EFSEEK’
     SDL_EFSEEK,
     ^~~~~~~~~~
In file included from src/libs/SDL/include/SDL_audio.h:32:0,
                 from src/libs/SDL/include/SDL.h:36,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_error.h:60:5: note: previous declaration ‘SDL_errorcode SDL_EFSEEK’
     SDL_EFSEEK,
     ^~~~~~~~~~
In file included from /usr/include/SDL2/SDL_rwops.h:33:0,
                 from /usr/include/SDL2/SDL_mixer.h:28,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_error.h:61:5: error: redeclaration of ‘SDL_UNSUPPORTED’
     SDL_UNSUPPORTED,
     ^~~~~~~~~~~~~~~
In file included from src/libs/SDL/include/SDL_audio.h:32:0,
                 from src/libs/SDL/include/SDL.h:36,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_error.h:61:5: note: previous declaration ‘SDL_errorcode SDL_UNSUPPORTED’
     SDL_UNSUPPORTED,
     ^~~~~~~~~~~~~~~
In file included from /usr/include/SDL2/SDL_rwops.h:33:0,
                 from /usr/include/SDL2/SDL_mixer.h:28,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_error.h:62:5: error: redeclaration of ‘SDL_LASTERROR’
     SDL_LASTERROR
     ^~~~~~~~~~~~~
In file included from src/libs/SDL/include/SDL_audio.h:32:0,
                 from src/libs/SDL/include/SDL.h:36,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_error.h:62:5: note: previous declaration ‘SDL_errorcode SDL_LASTERROR’
     SDL_LASTERROR
     ^~~~~~~~~~~~~
In file included from /usr/include/SDL2/SDL_rwops.h:33:0,
                 from /usr/include/SDL2/SDL_mixer.h:28,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_error.h:63:3: error: conflicting declaration ‘typedef enum SDL_errorcode SDL_errorcode’
 } SDL_errorcode;
   ^~~~~~~~~~~~~
In file included from src/libs/SDL/include/SDL_audio.h:32:0,
                 from src/libs/SDL/include/SDL.h:36,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_error.h:63:3: note: previous declaration as ‘typedef enum SDL_errorcode SDL_errorcode’
 } SDL_errorcode;
   ^~~~~~~~~~~~~
In file included from /usr/include/SDL2/SDL_mixer.h:28:0,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_rwops.h:52:16: error: redefinition of ‘struct SDL_RWops’
 typedef struct SDL_RWops
                ^~~~~~~~~
In file included from src/libs/SDL/include/SDL_audio.h:36:0,
                 from src/libs/SDL/include/SDL.h:36,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_rwops.h:52:16: note: previous definition of ‘struct SDL_RWops’
 typedef struct SDL_RWops
                ^~~~~~~~~
In file included from /usr/include/SDL2/SDL_mixer.h:28:0,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_rwops.h:143:3: error: conflicting declaration ‘typedef int SDL_RWops’
 } SDL_RWops;
   ^~~~~~~~~
In file included from src/libs/SDL/include/SDL_audio.h:36:0,
                 from src/libs/SDL/include/SDL.h:36,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_rwops.h:143:3: note: previous declaration as ‘typedef struct SDL_RWops SDL_RWops’
 } SDL_RWops;
   ^~~~~~~~~
In file included from /usr/include/SDL2/SDL_audio.h:33:0,
                 from /usr/include/SDL2/SDL_mixer.h:29,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_endian.h: In function ‘Uint16 SDL_Swap16(Uint16)’:
/usr/include/SDL2/SDL_endian.h:78:1: error: redefinition of ‘Uint16 SDL_Swap16(Uint16)’
 SDL_Swap16(Uint16 x)
 ^~~~~~~~~~
In file included from src/libs/SDL/include/SDL_audio.h:33:0,
                 from src/libs/SDL/include/SDL.h:36,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_endian.h:78:1: note: ‘Uint16 SDL_Swap16(Uint16)’ previously defined here
 SDL_Swap16(Uint16 x)
 ^~~~~~~~~~
In file included from /usr/include/SDL2/SDL_audio.h:33:0,
                 from /usr/include/SDL2/SDL_mixer.h:29,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_endian.h: In function ‘Uint32 SDL_Swap32(Uint32)’:
/usr/include/SDL2/SDL_endian.h:122:1: error: redefinition of ‘Uint32 SDL_Swap32(Uint32)’
 SDL_Swap32(Uint32 x)
 ^~~~~~~~~~
In file included from src/libs/SDL/include/SDL_audio.h:33:0,
                 from src/libs/SDL/include/SDL.h:36,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_endian.h:116:1: note: ‘Uint32 SDL_Swap32(Uint32)’ previously defined here
 SDL_Swap32(Uint32 x)
 ^~~~~~~~~~
In file included from /usr/include/SDL2/SDL_audio.h:33:0,
                 from /usr/include/SDL2/SDL_mixer.h:29,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_endian.h: In function ‘Uint64 SDL_Swap64(Uint64)’:
/usr/include/SDL2/SDL_endian.h:189:1: error: redefinition of ‘Uint64 SDL_Swap64(Uint64)’
 SDL_Swap64(Uint64 x)
 ^~~~~~~~~~
In file included from src/libs/SDL/include/SDL_audio.h:33:0,
                 from src/libs/SDL/include/SDL.h:36,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_endian.h:168:1: note: ‘Uint64 SDL_Swap64(Uint64)’ previously defined here
 SDL_Swap64(Uint64 x)
 ^~~~~~~~~~
In file included from /usr/include/SDL2/SDL_audio.h:33:0,
                 from /usr/include/SDL2/SDL_mixer.h:29,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_endian.h: In function ‘float SDL_SwapFloat(float)’:
/usr/include/SDL2/SDL_endian.h:213:1: error: redefinition of ‘float SDL_SwapFloat(float)’
 SDL_SwapFloat(float x)
 ^~~~~~~~~~~~~
In file included from src/libs/SDL/include/SDL_audio.h:33:0,
                 from src/libs/SDL/include/SDL.h:36,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_endian.h:192:1: note: ‘float SDL_SwapFloat(float)’ previously defined here
 SDL_SwapFloat(float x)
 ^~~~~~~~~~~~~
In file included from /usr/include/SDL2/SDL_thread.h:35:0,
                 from /usr/include/SDL2/SDL_audio.h:35,
                 from /usr/include/SDL2/SDL_mixer.h:29,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_atomic.h: At global scope:
/usr/include/SDL2/SDL_atomic.h:195:31: error: conflicting declaration ‘typedef struct SDL_atomic_t SDL_atomic_t’
 typedef struct { int value; } SDL_atomic_t;
                               ^~~~~~~~~~~~
In file included from src/libs/SDL/include/SDL.h:35:0,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_atomic.h:189:31: note: previous declaration as ‘typedef struct SDL_atomic_t SDL_atomic_t’
 typedef struct { int value; } SDL_atomic_t;
                               ^~~~~~~~~~~~
In file included from /usr/include/SDL2/SDL_audio.h:35:0,
                 from /usr/include/SDL2/SDL_mixer.h:29,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_thread.h:60:5: error: redeclaration of ‘SDL_THREAD_PRIORITY_LOW’
     SDL_THREAD_PRIORITY_LOW,
     ^~~~~~~~~~~~~~~~~~~~~~~
In file included from src/libs/SDL/include/SDL_audio.h:35:0,
                 from src/libs/SDL/include/SDL.h:36,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_thread.h:60:5: note: previous declaration ‘SDL_ThreadPriority SDL_THREAD_PRIORITY_LOW’
     SDL_THREAD_PRIORITY_LOW,
     ^~~~~~~~~~~~~~~~~~~~~~~
In file included from /usr/include/SDL2/SDL_audio.h:35:0,
                 from /usr/include/SDL2/SDL_mixer.h:29,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_thread.h:61:5: error: redeclaration of ‘SDL_THREAD_PRIORITY_NORMAL’
     SDL_THREAD_PRIORITY_NORMAL,
     ^~~~~~~~~~~~~~~~~~~~~~~~~~
In file included from src/libs/SDL/include/SDL_audio.h:35:0,
                 from src/libs/SDL/include/SDL.h:36,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_thread.h:61:5: note: previous declaration ‘SDL_ThreadPriority SDL_THREAD_PRIORITY_NORMAL’
     SDL_THREAD_PRIORITY_NORMAL,
     ^~~~~~~~~~~~~~~~~~~~~~~~~~
In file included from /usr/include/SDL2/SDL_audio.h:35:0,
                 from /usr/include/SDL2/SDL_mixer.h:29,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_thread.h:62:5: error: redeclaration of ‘SDL_THREAD_PRIORITY_HIGH’
     SDL_THREAD_PRIORITY_HIGH
     ^~~~~~~~~~~~~~~~~~~~~~~~
In file included from src/libs/SDL/include/SDL_audio.h:35:0,
                 from src/libs/SDL/include/SDL.h:36,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_thread.h:62:5: note: previous declaration ‘SDL_ThreadPriority SDL_THREAD_PRIORITY_HIGH’
     SDL_THREAD_PRIORITY_HIGH
     ^~~~~~~~~~~~~~~~~~~~~~~~
In file included from /usr/include/SDL2/SDL_audio.h:35:0,
                 from /usr/include/SDL2/SDL_mixer.h:29,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_thread.h:63:3: error: conflicting declaration ‘typedef enum SDL_ThreadPriority SDL_ThreadPriority’
 } SDL_ThreadPriority;
   ^~~~~~~~~~~~~~~~~~
In file included from src/libs/SDL/include/SDL_audio.h:35:0,
                 from src/libs/SDL/include/SDL.h:36,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_thread.h:63:3: note: previous declaration as ‘typedef enum SDL_ThreadPriority SDL_ThreadPriority’
 } SDL_ThreadPriority;
   ^~~~~~~~~~~~~~~~~~
In file included from /usr/include/SDL2/SDL_mixer.h:29:0,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_audio.h:168:16: error: redefinition of ‘struct SDL_AudioSpec’
 typedef struct SDL_AudioSpec
                ^~~~~~~~~~~~~
In file included from src/libs/SDL/include/SDL.h:36:0,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_audio.h:168:16: note: previous definition of ‘struct SDL_AudioSpec’
 typedef struct SDL_AudioSpec
                ^~~~~~~~~~~~~
In file included from /usr/include/SDL2/SDL_mixer.h:29:0,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_audio.h:179:3: error: conflicting declaration ‘typedef int SDL_AudioSpec’
 } SDL_AudioSpec;
   ^~~~~~~~~~~~~
In file included from src/libs/SDL/include/SDL.h:36:0,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_audio.h:179:3: note: previous declaration as ‘typedef struct SDL_AudioSpec SDL_AudioSpec’
 } SDL_AudioSpec;
   ^~~~~~~~~~~~~
In file included from /usr/include/SDL2/SDL_mixer.h:29:0,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_audio.h:216:16: error: redefinition of ‘struct SDL_AudioCVT’
 typedef struct SDL_AudioCVT
                ^~~~~~~~~~~~
In file included from src/libs/SDL/include/SDL.h:36:0,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_audio.h:200:16: note: previous definition of ‘struct SDL_AudioCVT’
 typedef struct SDL_AudioCVT
                ^~~~~~~~~~~~
In file included from /usr/include/SDL2/SDL_mixer.h:29:0,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_audio.h:229:23: warning: ‘packed’ attribute ignored [-Wattributes]
 } SDL_AUDIOCVT_PACKED SDL_AudioCVT;
                       ^~~~~~~~~~~~
/usr/include/SDL2/SDL_audio.h:229:23: error: conflicting declaration ‘typedef int SDL_AudioCVT’
In file included from src/libs/SDL/include/SDL.h:36:0,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_audio.h:213:23: note: previous declaration as ‘typedef struct SDL_AudioCVT SDL_AudioCVT’
 } SDL_AUDIOCVT_PACKED SDL_AudioCVT;
                       ^~~~~~~~~~~~
In file included from /usr/include/SDL2/SDL_mixer.h:29:0,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_audio.h:387:25: error: redeclaration of ‘SDL_AUDIO_STOPPED’
     SDL_AUDIO_STOPPED = 0,
                         ^
In file included from src/libs/SDL/include/SDL.h:36:0,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_audio.h:370:5: note: previous declaration ‘SDL_AudioStatus SDL_AUDIO_STOPPED’
     SDL_AUDIO_STOPPED = 0,
     ^~~~~~~~~~~~~~~~~
In file included from /usr/include/SDL2/SDL_mixer.h:29:0,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_audio.h:388:5: error: redeclaration of ‘SDL_AUDIO_PLAYING’
     SDL_AUDIO_PLAYING,
     ^~~~~~~~~~~~~~~~~
In file included from src/libs/SDL/include/SDL.h:36:0,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_audio.h:371:5: note: previous declaration ‘SDL_AudioStatus SDL_AUDIO_PLAYING’
     SDL_AUDIO_PLAYING,
     ^~~~~~~~~~~~~~~~~
In file included from /usr/include/SDL2/SDL_mixer.h:29:0,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_audio.h:389:5: error: redeclaration of ‘SDL_AUDIO_PAUSED’
     SDL_AUDIO_PAUSED
     ^~~~~~~~~~~~~~~~
In file included from src/libs/SDL/include/SDL.h:36:0,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_audio.h:372:5: note: previous declaration ‘SDL_AudioStatus SDL_AUDIO_PAUSED’
     SDL_AUDIO_PAUSED
     ^~~~~~~~~~~~~~~~
In file included from /usr/include/SDL2/SDL_mixer.h:29:0,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_audio.h:390:3: error: conflicting declaration ‘typedef enum SDL_AudioStatus SDL_AudioStatus’
 } SDL_AudioStatus;
   ^~~~~~~~~~~~~~~
In file included from src/libs/SDL/include/SDL.h:36:0,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_audio.h:373:3: note: previous declaration as ‘typedef enum SDL_AudioStatus SDL_AudioStatus’
 } SDL_AudioStatus;
   ^~~~~~~~~~~~~~~
In file included from /usr/include/SDL2/SDL_mixer.h:31:0,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_version.h:51:16: error: redefinition of ‘struct SDL_version’
 typedef struct SDL_version
                ^~~~~~~~~~~
In file included from src/libs/SDL/include/SDL.h:57:0,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_version.h:51:16: note: previous definition of ‘struct SDL_version’
 typedef struct SDL_version
                ^~~~~~~~~~~
In file included from /usr/include/SDL2/SDL_mixer.h:31:0,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:12:
/usr/include/SDL2/SDL_version.h:56:3: error: conflicting declaration ‘typedef int SDL_version’
 } SDL_version;
   ^~~~~~~~~~~
In file included from src/libs/SDL/include/SDL.h:57:0,
                 from src/engine/common/ports/ISystem.h:8,
                 from src/engine/common/FileSystem.h:4,
                 from src/engine/client/sound/sdl/SDLSoundEngine.cpp:2:
src/libs/SDL/include/SDL_version.h:56:3: note: previous declaration as ‘typedef struct SDL_version SDL_version’
 } SDL_version;
   ^~~~~~~~~~~
make: *** [Makefile:212: /tmp/yaourt-tmp-owner/aur-caveexpress/caveexpress/engine/client/sound/sdl/SDLSoundEngine.cpp.o] Error 1
```
