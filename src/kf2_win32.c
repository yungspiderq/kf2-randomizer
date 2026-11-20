/* Killing Floor 2 Randomizer — fully native, offline Win32 desktop edition.
   No HTML, no browser, no Python runtime, no external DLLs.
   Build using clang-cl/lld-link (scripts included in tools/).
   Copyright 2026. MIT License. */

typedef unsigned short WORD, WCHAR, ATOM;
typedef unsigned int UINT, DWORD, COLORREF;
typedef long LONG;
typedef unsigned long long ULONG_PTR, WPARAM, SIZE_T, ULONGLONG;
typedef long long LONG_PTR, LPARAM, LRESULT;
typedef void *HANDLE, *HWND, *HINSTANCE, *HMENU, *HDC, *HBRUSH, *HFONT, *HGDIOBJ, *HCURSOR, *HICON;
typedef const WCHAR *LPCWSTR;
typedef WCHAR *LPWSTR;
typedef int BOOL;
typedef struct { LONG left,top,right,bottom; } RECT;
typedef struct { LONG x,y; } POINT;
typedef struct { HWND hwnd; UINT message; WPARAM wParam; LPARAM lParam; DWORD time; POINT pt; DWORD lPrivate; } MSG;
typedef struct { UINT cbSize; UINT style; void *lpfnWndProc; int cbClsExtra,cbWndExtra; HINSTANCE hInstance; HICON hIcon; HCURSOR hCursor; HBRUSH hbrBackground; LPCWSTR lpszMenuName,lpszClassName; HICON hIconSm; } WNDCLASSEXW;
typedef struct { HDC hdc; BOOL fErase; RECT rcPaint; BOOL fRestore; BOOL fIncUpdate; unsigned char rgbReserved[32]; } PAINTSTRUCT;
typedef struct { UINT CtlType,CtlID,itemID,itemAction,itemState; HWND hwndItem; HDC hDC; RECT rcItem; ULONG_PTR itemData; } DRAWITEMSTRUCT;
typedef struct { WORD wYear,wMonth,wDayOfWeek,wDay,wHour,wMinute,wSecond,wMilliseconds; } SYSTEMTIME;

__declspec(dllimport) HINSTANCE __stdcall GetModuleHandleW(LPCWSTR);
__declspec(dllimport) ATOM __stdcall RegisterClassExW(const WNDCLASSEXW*);
__declspec(dllimport) HWND __stdcall CreateWindowExW(DWORD,LPCWSTR,LPCWSTR,DWORD,int,int,int,int,HWND,HMENU,HINSTANCE,void*);
__declspec(dllimport) LRESULT __stdcall DefWindowProcW(HWND,UINT,WPARAM,LPARAM);
__declspec(dllimport) BOOL __stdcall ShowWindow(HWND,int);
__declspec(dllimport) BOOL __stdcall UpdateWindow(HWND);
__declspec(dllimport) BOOL __stdcall GetMessageW(MSG*,HWND,UINT,UINT);
__declspec(dllimport) BOOL __stdcall TranslateMessage(const MSG*);
__declspec(dllimport) LRESULT __stdcall DispatchMessageW(const MSG*);
__declspec(dllimport) void __stdcall PostQuitMessage(int);
__declspec(dllimport) LRESULT __stdcall SendMessageW(HWND,UINT,WPARAM,LPARAM);
__declspec(dllimport) BOOL __stdcall MoveWindow(HWND,int,int,int,int,BOOL);
__declspec(dllimport) BOOL __stdcall SetWindowTextW(HWND,LPCWSTR);
__declspec(dllimport) HWND __stdcall SetFocus(HWND);
__declspec(dllimport) HCURSOR __stdcall LoadCursorW(HINSTANCE,LPCWSTR);
__declspec(dllimport) HDC __stdcall BeginPaint(HWND,PAINTSTRUCT*);
__declspec(dllimport) BOOL __stdcall EndPaint(HWND,const PAINTSTRUCT*);
__declspec(dllimport) BOOL __stdcall FillRect(HDC,const RECT*,HBRUSH);
__declspec(dllimport) BOOL __stdcall GetClientRect(HWND,RECT*);
__declspec(dllimport) BOOL __stdcall InvalidateRect(HWND,const RECT*,BOOL);
__declspec(dllimport) BOOL __stdcall DrawTextW(HDC,LPCWSTR,int,RECT*,UINT);
__declspec(dllimport) BOOL __stdcall OpenClipboard(HWND);
__declspec(dllimport) BOOL __stdcall EmptyClipboard(void);
__declspec(dllimport) HANDLE __stdcall SetClipboardData(UINT,HANDLE);
__declspec(dllimport) BOOL __stdcall CloseClipboard(void);
__declspec(dllimport) int __stdcall MessageBoxW(HWND,LPCWSTR,LPCWSTR,UINT);
__declspec(dllimport) DWORD __stdcall GetEnvironmentVariableW(LPCWSTR,LPWSTR,DWORD);
__declspec(dllimport) BOOL __stdcall CreateDirectoryW(LPCWSTR,void*);
__declspec(dllimport) UINT __stdcall GetPrivateProfileIntW(LPCWSTR,LPCWSTR,int,LPCWSTR);
__declspec(dllimport) DWORD __stdcall GetPrivateProfileStringW(LPCWSTR,LPCWSTR,LPCWSTR,LPWSTR,DWORD,LPCWSTR);
__declspec(dllimport) BOOL __stdcall WritePrivateProfileStringW(LPCWSTR,LPCWSTR,LPCWSTR,LPCWSTR);
__declspec(dllimport) ULONGLONG __stdcall GetTickCount64(void);
__declspec(dllimport) void __stdcall GetLocalTime(SYSTEMTIME*);
__declspec(dllimport) void __stdcall ExitProcess(DWORD);
__declspec(dllimport) HANDLE __stdcall GlobalAlloc(UINT,SIZE_T);
__declspec(dllimport) void * __stdcall GlobalLock(HANDLE);
__declspec(dllimport) BOOL __stdcall GlobalUnlock(HANDLE);
__declspec(dllimport) HANDLE __stdcall GlobalFree(HANDLE);
__declspec(dllimport) HBRUSH __stdcall CreateSolidBrush(COLORREF);
__declspec(dllimport) HFONT __stdcall CreateFontW(int,int,int,int,int,DWORD,DWORD,DWORD,DWORD,DWORD,DWORD,DWORD,DWORD,LPCWSTR);
__declspec(dllimport) HGDIOBJ __stdcall SelectObject(HDC,HGDIOBJ);
__declspec(dllimport) BOOL __stdcall DeleteObject(HGDIOBJ);
__declspec(dllimport) COLORREF __stdcall SetTextColor(HDC,COLORREF);
__declspec(dllimport) COLORREF __stdcall SetBkColor(HDC,COLORREF);
__declspec(dllimport) int __stdcall SetBkMode(HDC,int);
__declspec(dllimport) BOOL __stdcall RoundRect(HDC,int,int,int,int,int,int);
__declspec(dllimport) HGDIOBJ __stdcall GetStockObject(int);

#define WS_OVERLAPPEDWINDOW 0x00CF0000u
#define WS_VISIBLE 0x10000000u
#define WS_CHILD 0x40000000u
#define WS_VSCROLL 0x00200000u
#define WS_TABSTOP 0x00010000u
#define WS_BORDER 0x00800000u
#define WS_EX_CLIENTEDGE 0x00000200u
#define WS_CLIPCHILDREN 0x02000000u
#define BS_AUTOCHECKBOX 0x00000003u
#define BS_OWNERDRAW 0x0000000Bu
#define SS_LEFT 0
#define SS_NOPREFIX 0x80
#define CBS_DROPDOWNLIST 0x0003u
#define CBS_HASSTRINGS 0x0200u
#define LBS_NOTIFY 0x0001u
#define LBS_NOINTEGRALHEIGHT 0x0100u
#define WM_CREATE 0x0001
#define WM_DESTROY 0x0002
#define WM_SIZE 0x0005
#define WM_PAINT 0x000F
#define WM_CLOSE 0x0010
#define WM_COMMAND 0x0111
#define WM_DRAWITEM 0x002B
#define WM_CTLCOLORSTATIC 0x0138
#define WM_CTLCOLORBTN 0x0135
#define WM_CTLCOLORLISTBOX 0x0134
#define WM_ERASEBKGND 0x0014
#define WM_SETFONT 0x0030
#define BN_CLICKED 0
#define LBN_DBLCLK 2
#define BM_GETCHECK 0x00F0
#define BM_SETCHECK 0x00F1
#define BST_CHECKED 1
#define CB_ADDSTRING 0x0143
#define CB_GETCURSEL 0x0147
#define CB_SETCURSEL 0x014E
#define LB_ADDSTRING 0x0180
#define LB_RESETCONTENT 0x0184
#define LB_GETCURSEL 0x0188
#define DT_LEFT 0
#define DT_CENTER 1
#define DT_VCENTER 4
#define DT_SINGLELINE 0x20
#define DT_END_ELLIPSIS 0x8000
#define CF_UNICODETEXT 13
#define GMEM_MOVEABLE 0x0002
#define SW_SHOW 5
#define TRANSPARENT 1
#define IDYES 6
#define MB_YESNO 4
#define MB_ICONQUESTION 0x20
#define FONT_WEIGHT_BOLD 700
#define RGB_(r,g,b) ((COLORREF)((r)|((g)<<8)|((b)<<16)))
#define WM_USER 0x0400
#define MIN(a,b) ((a)<(b)?(a):(b))

/* Compiler may lower large structure assignments to memcpy. Avoid a CRT dependency. */
void *memcpy(void *dst,const void *src,SIZE_T n){ unsigned char*d=(unsigned char*)dst;const unsigned char*s=(const unsigned char*)src;while(n--)*d++=*s++;return dst;}

#define ID_GENERATE 100
#define ID_SKILLS 101
#define ID_COPY 102
#define ID_CLEAR 103
#define ID_ALL 104
#define ID_NONE 105
#define ID_HISTORY 106
#define ID_CB_START 200
#define ID_MAPON 220
#define ID_SKILLON 221
#define ID_SMART 222
#define ID_SOLO 223
#define ID_DIFF 230
#define ID_LENGTH 231
#define ID_CHALLENGE 232

static const WCHAR *perks[10]={L"Берсеркер",L"Коммандос",L"Поддержка",L"Полевой медик",L"Подрывник",L"Поджигатель",L"Стрелок",L"Снайпер",L"Спецназ",L"Выживальщик"};
static const WCHAR *namesEn[10]={L"BERSERKER",L"COMMANDO",L"SUPPORT",L"FIELD MEDIC",L"DEMOLITIONIST",L"FIREBUG",L"GUNSLINGER",L"SHARPSHOOTER",L"SWAT",L"SURVIVALIST"};
static const WCHAR *maps[27]={L"Ashwood Asylum",L"Biolapse",L"Biotics Lab",L"Black Forest",L"Burning Paris",L"Catacombs",L"Containment Station",L"Desolation",L"Dystopia 2029",L"Elysium",L"Evacuation Point",L"Farmhouse",L"Hellmark Station",L"Hostile Grounds",L"Moonbase",L"Monster Ball",L"Netherhold",L"Nightmare",L"Nuked",L"Outpost",L"Prison",L"Sanitarium",L"Shopping Spree",L"Steam Fortress",L"The Tragic Kingdom",L"Volter Manor",L"Zed Landing"};
static const WCHAR *diffs[4]={L"Normal",L"Hard",L"Suicidal",L"Hell on Earth"};
static const WCHAR *lengths[3]={L"Короткий · 4 волны",L"Средний · 7 волн",L"Длинный · 10 волн"};
typedef struct {int level, perk; const WCHAR *text; int solo_ok;} Challenge;
static const Challenge challenges[]={
 {0,-1,L"Не меняй класс на протяжении первых трёх волн.",1},
 {0,-1,L"Заверши весь матч на выпавшем классе.",1},
 {0,-1,L"Используй первую случайную ветку навыков до босса.",1},
 {0,-1,L"На протяжении двух волн не меняй оружие.",1},
 {0,-1,L"Сыграй две волны с одним и тем же набором навыков.",1},
 {0,-1,L"Не покупай оружие во время ближайшей торговой фазы.",1},
 {1,-1,L"Продержись пять волн, не меняя класс.",1},
 {1,-1,L"Сыграй весь матч с фиксированной веткой навыков.",1},
 {1,-1,L"Выиграй раунд с единственным основным оружием.",1},
 {1,-1,L"Попробуй продержаться две волны без брони.",1},
 {1,-1,L"Проведи весь матч с одним типом основного оружия.",1},
 {1,-1,L"Пройди три волны без смены оружейного набора.",1},
 {2,-1,L"Победи босса на изначально сгенерированном классе.",1},
 {2,-1,L"Заверши матч без смены оружия после первой покупки.",1},
 {2,-1,L"Выиграй две партии подряд одним классом.",1},
 {2,-1,L"Заверши матч, ни разу не меняя ветку навыков.",1},
 {1,0,L"Проведи три волны только в ближнем бою.",1},
 {1,1,L"Отмечай невидимых врагов для своей команды каждую волну.",0},
 {1,2,L"Помоги союзникам пережить три волны подряд.",0},
 {0,3,L"Каждую волну лечи минимум одного союзника.",0},
 {1,4,L"Используй навыки подрывника до самого босса.",1},
 {1,5,L"Сыграй три волны с одним основным огненным оружием.",1},
 {1,6,L"Используй только парное оружие две волны подряд.",1},
 {1,7,L"Не меняй выбранную ветку навыков весь матч.",1},
 {1,8,L"Проведи три волны, используя оружие своего класса.",1},
 {1,9,L"В течение матча испробуй три разных типа оружия.",1}
};
#define CHALLENGE_COUNT 26

typedef struct {int perk, map, diff, length, skillBits, challenge; WCHAR when[22];} Result;
static Result history[80],current;
static int histCount=0,hasCurrent=0,bag[10],bagCount=0,lastPerk=-1;
static HWND win, checks[10],mapOn,skillOn,smartOn,soloOn,diffCombo,lenCombo,chalCombo;
static HWND brand,version,labelClass,labelEng,labelSkill,labelMap,labelDiff,labelLen,labelChal,labelLevel,statusLine,historyList;
static HWND btnGen,btnSkill,btnCopy,btnClear,btnAll,btnNone;
static HWND staticUI[12];
static HFONT fontBase,fontSmall,fontBrand,fontHero,fontSection;
static HBRUSH bgBrush,panelBrush,heroBrush,fieldBrush;
static WCHAR configPath[540];
static unsigned long long rndState;
static int noPersist=0;

static unsigned int rng(void){
 rndState^=rndState<<13; rndState^=rndState>>7; rndState^=rndState<<17;
 return (unsigned int)(rndState>>32)^(unsigned int)rndState;
}
static int choose(int n){return n>1?(int)(rng()%(unsigned)n):0;}
static int wlen(const WCHAR*s){int n=0;while(s&&s[n])n++;return n;}
static void wcopy(WCHAR*dst,const WCHAR*src,int cap){int i=0; if(!src){dst[0]=0;return;}while(i<cap-1&&src[i]){dst[i]=src[i];i++;}dst[i]=0;}
static void wcat(WCHAR*dst,const WCHAR*src,int cap){int n=wlen(dst);wcopy(dst+n,src,cap-n);}
static void wnum(WCHAR*buf,int n){WCHAR temp[24];int z=0,k=0;if(n<0){buf[k++]=L'-';n=-n;}do{temp[z++]=(WCHAR)(L'0'+n%10);n/=10;}while(n);while(z)buf[k++]=temp[--z];buf[k]=0;}
static void appendNum(WCHAR*buf,int n,int cap){WCHAR t[26];wnum(t,n);wcat(buf,t,cap);}
static int parseNum(const WCHAR**p){int n=0,neg=0;if(**p==L'-'){neg=1;(*p)++;}while(**p>=L'0'&&**p<=L'9'){n=n*10+(**p-L'0');(*p)++;}if(**p==L'|')(*p)++;return neg?-n:n;}
static int check(HWND h){return SendMessageW(h,BM_GETCHECK,0,0)==BST_CHECKED;}
static void setCheck(HWND h,int b){SendMessageW(h,BM_SETCHECK,b?BST_CHECKED:0,0);}
static int selected(HWND h){return (int)SendMessageW(h,CB_GETCURSEL,0,0);}
static void setSelected(HWND h,int idx){SendMessageW(h,CB_SETCURSEL,(WPARAM)idx,0);}
static void set(HWND h,LPCWSTR s){SetWindowTextW(h,s);}
static void move(HWND h,int x,int y,int w,int height){if(h)MoveWindow(h,x,y,w>5?w:5,height>5?height:5,1);}
static HWND makeCtrl(LPCWSTR type,LPCWSTR text,DWORD style,int id){
 return CreateWindowExW(0,type,text,WS_CHILD|WS_VISIBLE|style,0,0,30,30,win,(HMENU)(ULONG_PTR)id,GetModuleHandleW(0),0);
}
static HWND makeLabel(LPCWSTR text,HFONT font){HWND h=makeCtrl(L"STATIC",text,SS_LEFT|SS_NOPREFIX,0);SendMessageW(h,WM_SETFONT,(WPARAM)font,1);return h;}
static HWND makeButton(LPCWSTR text,int id){HWND h=makeCtrl(L"BUTTON",text,BS_OWNERDRAW|WS_TABSTOP,id);SendMessageW(h,WM_SETFONT,(WPARAM)fontBase,1);return h;}
static HWND makeCheck(LPCWSTR text,int id){HWND h=makeCtrl(L"BUTTON",text,BS_AUTOCHECKBOX|WS_TABSTOP,id);SendMessageW(h,WM_SETFONT,(WPARAM)fontBase,1);return h;}
static HWND makeCombo(int id){HWND h=makeCtrl(L"COMBOBOX",L"",CBS_DROPDOWNLIST|CBS_HASSTRINGS|WS_TABSTOP,id);SendMessageW(h,WM_SETFONT,(WPARAM)fontBase,1);return h;}
static void comboAdd(HWND h,LPCWSTR text){SendMessageW(h,CB_ADDSTRING,0,(LPARAM)text);}
static void updateStatus(LPCWSTR message){set(statusLine,message);}
static void stamp(WCHAR*out){SYSTEMTIME t;GetLocalTime(&t);out[0]=0;appendNum(out,t.wDay,22);wcat(out,L".",22);appendNum(out,t.wMonth,22);wcat(out,L".",22);appendNum(out,t.wYear,22);wcat(out,L"  ",22);if(t.wHour<10)wcat(out,L"0",22);appendNum(out,t.wHour,22);wcat(out,L":",22);if(t.wMinute<10)wcat(out,L"0",22);appendNum(out,t.wMinute,22);}

static void iniWriteInt(LPCWSTR section,LPCWSTR key,int val){WCHAR b[26];wnum(b,val);WritePrivateProfileStringW(section,key,b,configPath);}
static int iniInt(LPCWSTR section,LPCWSTR key,int def){return (int)GetPrivateProfileIntW(section,key,def,configPath);}
static void configInit(void){
 WCHAR root[400],dir[500]; DWORD z=GetEnvironmentVariableW(L"APPDATA",root,400);
 if(z<1||z>=400)wcopy(root,L".",400);
 wcopy(dir,root,500);wcat(dir,L"\\KF2 Randomizer",500);CreateDirectoryW(dir,0);
 wcopy(configPath,dir,540);wcat(configPath,L"\\settings.ini",540);
}
static void saveConfig(void){
 int i;WCHAR key[30],val[160];
 if(noPersist)return;
 for(i=0;i<10;i++){wnum(key,i);iniWriteInt(L"classes",key,check(checks[i]));}
 iniWriteInt(L"settings",L"maps",check(mapOn));iniWriteInt(L"settings",L"skills",check(skillOn));
 iniWriteInt(L"settings",L"smart",check(smartOn));iniWriteInt(L"settings",L"solo",check(soloOn));
 iniWriteInt(L"settings",L"difficulty",selected(diffCombo));iniWriteInt(L"settings",L"length",selected(lenCombo));
 iniWriteInt(L"settings",L"challenge",selected(chalCombo));
 iniWriteInt(L"history",L"count",histCount);
 for(i=0;i<histCount;i++){
  wnum(key,i);val[0]=0;
  appendNum(val,history[i].perk,160);wcat(val,L"|",160);
  appendNum(val,history[i].map,160);wcat(val,L"|",160);
  appendNum(val,history[i].diff,160);wcat(val,L"|",160);
  appendNum(val,history[i].length,160);wcat(val,L"|",160);
  appendNum(val,history[i].skillBits,160);wcat(val,L"|",160);
  appendNum(val,history[i].challenge,160);wcat(val,L"|",160);
  wcat(val,history[i].when,160);
  WritePrivateProfileStringW(L"history",key,val,configPath);
 }
}
static void loadConfig(void){
 int i; WCHAR key[30],s[160];const WCHAR*p;
 noPersist=1;
 for(i=0;i<10;i++){wnum(key,i);setCheck(checks[i],iniInt(L"classes",key,1));}
 setCheck(mapOn,iniInt(L"settings",L"maps",1));setCheck(skillOn,iniInt(L"settings",L"skills",1));
 setCheck(smartOn,iniInt(L"settings",L"smart",1));setCheck(soloOn,iniInt(L"settings",L"solo",0));
 setSelected(diffCombo,MIN(4,iniInt(L"settings",L"difficulty",0)));
 setSelected(lenCombo,MIN(3,iniInt(L"settings",L"length",0)));
 setSelected(chalCombo,MIN(4,iniInt(L"settings",L"challenge",1)));
 histCount=iniInt(L"history",L"count",0);if(histCount<0)histCount=0;if(histCount>80)histCount=80;
 for(i=0;i<histCount;i++){
  wnum(key,i);s[0]=0;GetPrivateProfileStringW(L"history",key,L"",s,160,configPath);p=s;
  history[i].perk=parseNum(&p);history[i].map=parseNum(&p);history[i].diff=parseNum(&p);
  history[i].length=parseNum(&p);history[i].skillBits=parseNum(&p);history[i].challenge=parseNum(&p);
  wcopy(history[i].when,p,22);
  if(history[i].perk<0||history[i].perk>=10||history[i].map < -1 || history[i].map >= 27 || history[i].diff < 0 || history[i].diff >=4 || history[i].length <0 || history[i].length>=3 || history[i].challenge< -1 || history[i].challenge>=CHALLENGE_COUNT){histCount=i;break;}
 }
 noPersist=0;
}
static int choosePerk(void){
 int available[10],a=0,i,j,v;
 for(i=0;i<10;i++)if(check(checks[i]))available[a++]=i;
 if(!a){MessageBoxW(win,L"Включи хотя бы один класс слева.",L"KF2 Randomizer",0x30);return -1;}
 if(!check(smartOn))return available[choose(a)];
 for(i=0;i<bagCount;){int found=0;for(j=0;j<a;j++)if(bag[i]==available[j])found=1;if(found)i++;else{bag[i]=bag[--bagCount];}}
 if(!bagCount){for(i=0;i<a;i++)bag[i]=available[i];bagCount=a;for(i=a-1;i>0;i--){j=choose(i+1);v=bag[i];bag[i]=bag[j];bag[j]=v;}
  if(a>1 && bag[a-1]==lastPerk){v=bag[a-1];bag[a-1]=bag[0];bag[0]=v;}
 }
 return bag[--bagCount];
}
static int chooseChallenge(int perk){
 int candidates[CHALLENGE_COUNT],a=0,i,filter=selected(chalCombo);
 if(filter==0)return -1;
 for(i=0;i<CHALLENGE_COUNT;i++){
  if(challenges[i].perk!=-1 && challenges[i].perk!=perk)continue;
  if(check(soloOn)&&!challenges[i].solo_ok)continue;
  if(filter>=2 && challenges[i].level!=(filter-2))continue;
  candidates[a++]=i;
 }
 if(!a)return -1;
 return candidates[choose(a)];
}
static void skillsText(int bits,WCHAR*out){int i;const int levels[5]={5,10,15,20,25};out[0]=0;
 if(bits<0){wcat(out,L"Свободный выбор",140);return;}
 for(i=0;i<5;i++){appendNum(out,levels[i],140);wcat(out,L": ",140);wcat(out,(bits&(1<<i))?L"П":L"Л",140);if(i<4)wcat(out,L"     ",140);}
}
static void showResult(Result *r){WCHAR s[140];
 if(!r)return;
 set(labelClass,perks[r->perk]);set(labelEng,namesEn[r->perk]);
 skillsText(r->skillBits,s);set(labelSkill,s);
 set(labelMap,r->map<0?L"Свободный выбор":maps[r->map]);
 set(labelDiff,diffs[r->diff]);set(labelLen,lengths[r->length]);
 set(labelChal,r->challenge<0?L"Без испытания":challenges[r->challenge].text);
 set(labelLevel,r->challenge<0?L"Без дополнительных ограничений":
   challenges[r->challenge].level==0?L"СЛОЖНОСТЬ: ЛЁГКАЯ":
   challenges[r->challenge].level==1?L"СЛОЖНОСТЬ: СРЕДНЯЯ":L"СЛОЖНОСТЬ: ВЫСОКАЯ");
}
static void refreshHistory(void){int i;WCHAR s[260];
 SendMessageW(historyList,LB_RESETCONTENT,0,0);
 for(i=0;i<histCount;i++){
  s[0]=0;wcat(s,history[i].when,260);wcat(s,L"    ·    ",260);
  wcat(s,perks[history[i].perk],260);wcat(s,L"   /   ",260);
  wcat(s,history[i].map<0?L"Без карты":maps[history[i].map],260);
  SendMessageW(historyList,LB_ADDSTRING,0,(LPARAM)s);
 }
}
static void pushResult(Result r){int i;
 for(i=MIN(histCount,79);i>0;i--)history[i]=history[i-1];
 history[0]=r;histCount=MIN(histCount+1,80);
 current=r;hasCurrent=1;lastPerk=r.perk;showResult(&r);refreshHistory();saveConfig();
}
static void generate(void){Result r;int perk=choosePerk();if(perk<0)return;
 r.perk=perk;
 r.map=check(mapOn)?choose(27):-1;
 r.diff=selected(diffCombo)-1;if(r.diff<0)r.diff=choose(4);
 r.length=selected(lenCombo)-1;if(r.length<0)r.length=choose(3);
 r.skillBits=check(skillOn)?choose(32):-1;
 r.challenge=chooseChallenge(perk);stamp(r.when);pushResult(r);
 updateStatus(L"Новый случайный набор готов.");
}
static void rerollSkills(void){Result r;if(!hasCurrent)return;r=current;
 if(!check(skillOn)){updateStatus(L"Включи генерацию навыков в настройках.");return;}
 r.skillBits=choose(32);if(r.skillBits==current.skillBits)r.skillBits=(r.skillBits+1)%32;
 stamp(r.when);pushResult(r);updateStatus(L"Ветка навыков изменена.");
}
static void copyCurrent(void){WCHAR s[1100],skills[140];HANDLE m;WCHAR*data;int i,n;
 if(!hasCurrent)return;
 skillsText(current.skillBits,skills);s[0]=0;
 wcat(s,L"KILLING FLOOR 2 — RANDOMIZER\r\nКласс: ",1100);wcat(s,perks[current.perk],1100);
 wcat(s,L"\r\nНавыки: ",1100);wcat(s,skills,1100);
 wcat(s,L"\r\nКарта: ",1100);wcat(s,current.map<0?L"Свободный выбор":maps[current.map],1100);
 wcat(s,L"\r\nСложность: ",1100);wcat(s,diffs[current.diff],1100);
 wcat(s,L"\r\nДлина: ",1100);wcat(s,lengths[current.length],1100);
 wcat(s,L"\r\nИспытание: ",1100);wcat(s,current.challenge<0?L"Нет":challenges[current.challenge].text,1100);
 wcat(s,L"\r\n",1100);
 if(!OpenClipboard(win)){updateStatus(L"Не удалось открыть буфер обмена.");return;}
 EmptyClipboard();n=wlen(s)+1;m=GlobalAlloc(GMEM_MOVEABLE,n*sizeof(WCHAR));
 if(m){data=(WCHAR*)GlobalLock(m);if(data){for(i=0;i<n;i++)data[i]=s[i];GlobalUnlock(m);if(!SetClipboardData(CF_UNICODETEXT,m))GlobalFree(m);else m=0;}}
 CloseClipboard();updateStatus(m?L"Ошибка копирования.":L"Результат скопирован в буфер обмена.");
}
static void layout(int w,int h){int x=22,side=300, right=x+side+25, rw=w-right-24,hw,wy;
 if(w<900)w=900;if(h<630)h=630;
 move(brand,x,18,w-280,42);move(version,w-190,23,160,26);
 move(staticUI[0],x,82,side,26);
 for(int i=0;i<10;i++)move(checks[i],x+5,111+i*30,side-5,27);
 move(btnAll,x,415,140,34);move(btnNone,x+151,415,140,34);
 move(staticUI[1],x,469,side,24);
 move(mapOn,x+5,495,side-5,25);move(skillOn,x+5,521,side-5,25);
 move(smartOn,x+5,547,side-5,25);move(soloOn,x+5,573,side-5,25);
 move(staticUI[2],x,612,94,23);move(diffCombo,x+104,609,side-104,205);
 move(staticUI[3],x,650,94,24);move(lenCombo,x+104,646,side-104,205);
 move(staticUI[4],x,688,94,24);move(chalCombo,x+104,684,side-104,205);
 // Right pane, scale vertically as the main window is resized.
 move(staticUI[5],right,84,rw,24);
 move(labelClass,right,112,rw,57);
 move(labelEng,right,170,rw,27);
 move(staticUI[6],right,218,rw/2-8,20);move(labelSkill,right,243,rw,35);
 move(staticUI[7],right,301,rw/2-10,22);move(staticUI[8],right+rw/2,301,rw/2,22);
 move(labelMap,right,328,rw/2-12,36);move(labelDiff,right+rw/2,328,rw/2,36);
 move(staticUI[9],right,392,rw/2,22);move(labelLen,right,418,rw,34);
 move(staticUI[10],right,469,rw,22);move(labelChal,right,500,rw,64);
 move(labelLevel,right,567,rw,21);
 move(btnGen,right,608,rw/2+12,50);move(btnSkill,right+rw/2+24,608,rw/2-24,50);
 move(btnCopy,right,669,180,38);move(btnClear,right+rw-170,669,170,38);
 wy=723;hw=h-wy-62;
 if(hw<35){ wy=MIN(723,h-96);hw=h-wy-54; }
 move(staticUI[11],right,wy-26,rw,24);
 move(historyList,right,wy,rw,hw);
 move(statusLine,right,h-27,rw,20);
}
static void drawButton(const DRAWITEMSTRUCT*di){int primary=(di->CtlID==ID_GENERATE);int down=(di->itemState&1);COLORREF c=primary?RGB_(215,63,55):(down?RGB_(58,64,75):RGB_(37,43,52));RECT r=di->rcItem;
 HBRUSH fill=CreateSolidBrush(c);HGDIOBJ old=SelectObject(di->hDC,(HGDIOBJ)fill);
 SelectObject(di->hDC,GetStockObject(8));RoundRect(di->hDC,r.left,r.top,r.right-1,r.bottom-1,13,13);
 SelectObject(di->hDC,old);DeleteObject((HGDIOBJ)fill);
 SetBkMode(di->hDC,TRANSPARENT);SetTextColor(di->hDC,RGB_(245,247,249));
 SelectObject(di->hDC,(HGDIOBJ)fontBase);
 WCHAR text[120];/* owner-draw text taken from id so no GetWindowText dependency */
 LPCWSTR t=L"";
 switch(di->CtlID){case ID_GENERATE:t=L"СГЕНЕРИРОВАТЬ";break;case ID_SKILLS:t=L"Перебросить навыки";break;
 case ID_COPY:t=L"Копировать";break;case ID_CLEAR:t=L"Очистить историю";break;case ID_ALL:t=L"Выбрать все";break;case ID_NONE:t=L"Снять все";break;}
 wcopy(text,t,120);DrawTextW(di->hDC,text,-1,&r,DT_CENTER|DT_VCENTER|DT_SINGLELINE);
}
static LRESULT __stdcall windowProc(HWND hwnd,UINT msg,WPARAM wp,LPARAM lp){
 switch(msg){
  case WM_CREATE:{
   win=hwnd;
   bgBrush=CreateSolidBrush(RGB_(17,20,25));panelBrush=CreateSolidBrush(RGB_(26,31,39));heroBrush=CreateSolidBrush(RGB_(34,26,29));fieldBrush=CreateSolidBrush(RGB_(34,40,50));
   fontBase=CreateFontW(17,0,0,0,500,0,0,0,1,0,0,0,0,L"Segoe UI");
   fontSmall=CreateFontW(15,0,0,0,400,0,0,0,1,0,0,0,0,L"Segoe UI");
   fontBrand=CreateFontW(27,0,0,0,700,0,0,0,1,0,0,0,0,L"Segoe UI");
   fontHero=CreateFontW(43,0,0,0,700,0,0,0,1,0,0,0,0,L"Segoe UI");
   fontSection=CreateFontW(16,0,0,0,700,0,0,0,1,0,0,0,0,L"Segoe UI");
   brand=makeLabel(L"KF2  /  RANDOMIZER",fontBrand);version=makeLabel(L"NATIVE DESKTOP  ·  0.3",fontSmall);
   staticUI[0]=makeLabel(L"01   ВЫБОР КЛАССОВ",fontSection);
   for(int i=0;i<10;i++)checks[i]=makeCheck(perks[i],ID_CB_START+i);
   btnAll=makeButton(L"Выбрать все",ID_ALL);btnNone=makeButton(L"Снять все",ID_NONE);
   staticUI[1]=makeLabel(L"02   НАСТРОЙКИ",fontSection);
   mapOn=makeCheck(L"Случайная карта",ID_MAPON);skillOn=makeCheck(L"Случайные навыки",ID_SKILLON);
   smartOn=makeCheck(L"Цикл классов без повторов",ID_SMART);soloOn=makeCheck(L"Одиночная игра",ID_SOLO);
   staticUI[2]=makeLabel(L"Сложность",fontSmall);staticUI[3]=makeLabel(L"Волны",fontSmall);staticUI[4]=makeLabel(L"Челлендж",fontSmall);
   diffCombo=makeCombo(ID_DIFF);lenCombo=makeCombo(ID_LENGTH);chalCombo=makeCombo(ID_CHALLENGE);
   comboAdd(diffCombo,L"Случайная");for(int i=0;i<4;i++)comboAdd(diffCombo,diffs[i]);
   comboAdd(lenCombo,L"Случайная");for(int i=0;i<3;i++)comboAdd(lenCombo,lengths[i]);
   comboAdd(chalCombo,L"Без испытания");comboAdd(chalCombo,L"Случайное");comboAdd(chalCombo,L"Лёгкий");comboAdd(chalCombo,L"Средний");comboAdd(chalCombo,L"Сложный");
   staticUI[5]=makeLabel(L"ТВОЙ СЛЕДУЮЩИЙ КЛАСС",fontSection);
   labelClass=makeLabel(L"—",fontHero);labelEng=makeLabel(L"",fontSmall);
   staticUI[6]=makeLabel(L"НАВЫКИ (5–25)",fontSection);labelSkill=makeLabel(L"—",fontBase);
   staticUI[7]=makeLabel(L"КАРТА",fontSection);staticUI[8]=makeLabel(L"СЛОЖНОСТЬ",fontSection);
   labelMap=makeLabel(L"—",fontBase);labelDiff=makeLabel(L"—",fontBase);
   staticUI[9]=makeLabel(L"ПРОДОЛЖИТЕЛЬНОСТЬ",fontSection);labelLen=makeLabel(L"—",fontBase);
   staticUI[10]=makeLabel(L"СЛУЧАЙНОЕ ИСПЫТАНИЕ",fontSection);labelChal=makeLabel(L"—",fontBase);labelLevel=makeLabel(L"",fontSmall);
   btnGen=makeButton(L"СГЕНЕРИРОВАТЬ",ID_GENERATE);btnSkill=makeButton(L"Перебросить навыки",ID_SKILLS);
   btnCopy=makeButton(L"Копировать",ID_COPY);btnClear=makeButton(L"Очистить историю",ID_CLEAR);
   staticUI[11]=makeLabel(L"ИСТОРИЯ  ·  двойной щелчок — открыть",fontSection);
   historyList=makeCtrl(L"LISTBOX",L"",WS_VSCROLL|WS_BORDER|LBS_NOTIFY|LBS_NOINTEGRALHEIGHT,ID_HISTORY);
   SendMessageW(historyList,WM_SETFONT,(WPARAM)fontSmall,1);
   statusLine=makeLabel(L"Рандомайзер работает локально и не изменяет игру.",fontSmall);
   configInit();loadConfig();refreshHistory();
   if(histCount){current=history[0];hasCurrent=1;lastPerk=current.perk;showResult(&current);}else generate();
   return 0;
  }
  case WM_SIZE:{RECT r;GetClientRect(hwnd,&r);layout(r.right,r.bottom);return 0;}
  case WM_ERASEBKGND:{RECT r;GetClientRect(hwnd,&r);FillRect((HDC)wp,&r,bgBrush);return 1;}
  case WM_CTLCOLORSTATIC:{HDC dc=(HDC)wp;SetBkColor(dc,RGB_(17,20,25));SetTextColor(dc,RGB_(228,232,238));SetBkMode(dc,TRANSPARENT);
   if((HWND)lp==labelClass)SetTextColor(dc,RGB_(252,245,243));
   else if((HWND)lp==labelLevel || (HWND)lp==version || (HWND)lp==statusLine)SetTextColor(dc,RGB_(142,151,168));
   else if((HWND)lp==labelEng)SetTextColor(dc,RGB_(233,101,91));
   return (LRESULT)bgBrush;}
  case WM_CTLCOLORBTN:{HDC dc=(HDC)wp;SetBkColor(dc,RGB_(17,20,25));SetTextColor(dc,RGB_(227,232,237));return (LRESULT)bgBrush;}
  case WM_CTLCOLORLISTBOX:{HDC dc=(HDC)wp;SetBkColor(dc,RGB_(26,31,39));SetTextColor(dc,RGB_(228,232,238));return (LRESULT)panelBrush;}
  case WM_DRAWITEM:{DRAWITEMSTRUCT*di=(DRAWITEMSTRUCT*)lp;if(di->CtlType==4){drawButton(di);return 1;}return 0;}
  case WM_COMMAND:{int id=(int)(wp&0xFFFF),code=(int)((wp>>16)&0xFFFF);
   if(id==ID_GENERATE&&code==BN_CLICKED)generate();
   else if(id==ID_SKILLS&&code==BN_CLICKED)rerollSkills();
   else if(id==ID_COPY&&code==BN_CLICKED)copyCurrent();
   else if(id==ID_ALL&&code==BN_CLICKED){for(int i=0;i<10;i++)setCheck(checks[i],1);bagCount=0;saveConfig();}
   else if(id==ID_NONE&&code==BN_CLICKED){for(int i=0;i<10;i++)setCheck(checks[i],0);bagCount=0;saveConfig();}
   else if(id==ID_CLEAR&&code==BN_CLICKED){if(MessageBoxW(win,L"Очистить всю историю случайных наборов?",L"KF2 Randomizer",MB_YESNO|MB_ICONQUESTION)==IDYES){histCount=0;refreshHistory();saveConfig();}}
   else if(id==ID_HISTORY && code==LBN_DBLCLK){int idx=(int)SendMessageW(historyList,LB_GETCURSEL,0,0);if(idx>=0&&idx<histCount){current=history[idx];hasCurrent=1;showResult(&current);updateStatus(L"Восстановлен результат из истории.");}}
   else if(id>=ID_CB_START&&id<ID_CB_START+10 && code==BN_CLICKED){bagCount=0;saveConfig();}
   else if(id>=ID_MAPON&&id<=ID_CHALLENGE)saveConfig();
   return 0;
  }
  case WM_CLOSE:saveConfig();return DefWindowProcW(hwnd,msg,wp,lp);
  case WM_DESTROY:PostQuitMessage(0);return 0;
 }
 return DefWindowProcW(hwnd,msg,wp,lp);
}
void WinMainCRTStartup(void){
 WNDCLASSEXW wc;MSG msg;HINSTANCE inst=GetModuleHandleW(0);
 rndState=GetTickCount64()^((ULONGLONG)(ULONG_PTR)inst<<13)^0xC4D12280961387A5ULL;
 wc.cbSize=sizeof(wc);wc.style=3;wc.lpfnWndProc=windowProc;wc.cbClsExtra=0;wc.cbWndExtra=0;
 wc.hInstance=inst;wc.hIcon=0;wc.hCursor=LoadCursorW(0,(LPCWSTR)32512);wc.hbrBackground=(HBRUSH)(ULONG_PTR)6;
 wc.lpszMenuName=0;wc.lpszClassName=L"KF2RandomizerNativeWindow";wc.hIconSm=0;
 if(!RegisterClassExW(&wc))ExitProcess(1);
 HWND hwnd=CreateWindowExW(0,wc.lpszClassName,L"Killing Floor 2 Randomizer  ·  Native Edition",WS_OVERLAPPEDWINDOW|WS_CLIPCHILDREN,
   90,65,1200,950,0,0,inst,0);
 if(!hwnd)ExitProcess(2);
 ShowWindow(hwnd,SW_SHOW);UpdateWindow(hwnd);
 while(GetMessageW(&msg,0,0,0)>0){TranslateMessage(&msg);DispatchMessageW(&msg);}
 ExitProcess(0);
}