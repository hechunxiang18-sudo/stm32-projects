#!/usr/bin/env python3
"""
生成智能家居系统电路原理图（嘉立创EDA/EasyEDA JSON格式 v6.x）
使用标准库元件符号，可在嘉立创EDA中直接打开编辑
"""
import json, os

OUTPUT = "E:/STM32/stm32-projects/iot/project-smart-home/schematic.json"

gid = [1]
def nid():
    gid[0] += 1; return gid[0] - 1

def new_uuid():
    import uuid; return uuid.uuid4().hex[:24].upper()

elements = []
shapes = []

# =============== 工具函数 ===============
def add_device(device, pkg, x, y, rot, name, value, w=10, h=10):
    """添加库元件"""
    e = {
        "gId": nid(), "package": pkg, "device": device,
        "x": x, "y": y, "rotation": rot, "locked": False,
        "span": {"x": w, "y": h},
        "config": {
            "uuid": new_uuid(),
            "name": name, "value": value,
            "spicePre": ""
        }
    }
    elements.append(e); return e

def add_wire(x1,y1,x2,y2, color="#000", w=1):
    shapes.append({"gId":nid(),"cmd":"WIRE","x1":x1,"y1":y1,"x2":x2,"y2":y2,"strokeWidth":w,"strokeColor":color,"layer":"Wire"})

def add_net(x,y,net,rot=0):
    shapes.append({"gId":nid(),"cmd":"NETLABEL","x":x,"y":y,"rotation":rot,"netName":net,"layer":"NetLabel"})

def add_text(x,y,txt, size=12, layer="Comment"):
    shapes.append({"gId":nid(),"cmd":"TEXT","x":x,"y":y,"rotation":0,"strokeWidth":0,"text":txt,"size":size,"layer":layer})

def add_rect(x,y,w,h, color, fill=None):
    shapes.append({"gId":nid(),"cmd":"RECT","x":x,"y":y,"w":w,"h":h,"strokeWidth":1.5,"strokeColor":color,"fillColor":fill or "transparent","layer":"Comment"})

# =============== 开始生成原理图 ===============
W, H = 2200, 1500

add_text(100,30, "智能家居中控系统 STM32F103C8T6 电路原理图", 20, "Title")
add_text(100,55, "V1.0  |  2026-06  |  DHT11+BH1750+ESP8266+4路继电器+OLED+红外", 13, "Comment")

# ==================== 1. 电源模块 ====================
add_rect(80,90,260,220, "#00796b", "rgba(0,121,107,0.04)")
add_text(100,100, "电源模块 Power", 14, "Comment")

# AMS1117-3.3
add_device("Device:AMS1117-3.3", "SOT-223", 200, 200, 0, "U5", "AMS1117-3.3", 30, 20)
add_text(140,180, "U5 AMS1117-3.3", 11, "Comment")
add_text(140,315, "Vin: 6.5-12V → 3.3V/800mA", 10, "Comment")

# 电容
add_device("Device:C", "0805", 80, 140, 0, "C1", "10uF")
add_device("Device:C", "0805", 80, 280, 0, "C2", "100nF")
add_device("Device:C", "0805", 320, 140, 0, "C3", "10uF")
add_device("Device:C", "0805", 320, 280, 0, "C4", "100nF")
add_device("Device:Cap_Pol", "SMD", 80, 360, 0, "C5", "100uF/16V")

add_text(50,135, "C1", 10); add_text(50,275, "C2", 10)
add_text(300,135, "C3", 10); add_text(300,275, "C4", 10)
add_text(50,355, "C5", 10)

# 电源网络
add_net(160, 100, "12V_IN")
add_net(160, 420, "GND")
add_net(360, 100, "3.3V")
add_net(360, 420, "GND")

# ==================== 2. STM32F103C8T6主控 ====================
add_rect(480,80,600,480, "#1565c0", "rgba(21,101,192,0.03)")
add_text(500,90, "主控 MCU - STM32F103C8T6 (LQFP-48)", 14, "Comment")

# 用文字描述引脚连接（这种方式在LCEDA里可读）
mcu_pins_desc = [
    (520,120, "PA0  → KEY1 (外部中断下降沿)"),
    (520,137, "PA1  → KEY2 (外部中断下降沿)"),
    (520,154, "PA2  → USART2_TX → ESP8266 RXD"),
    (520,171, "PA3  → USART2_RX → ESP8266 TXD"),
    (520,188, "PA9  → USART1_TX (调试串口)"),
    (520,205, "PA10 → USART1_RX (调试串口)"),
    (520,222, "PA13 → SWDIO (调试)"),
    (520,239, "PA14 → SWCLK (调试)"),
    (520,256, "PB0  → DHT11 Data (单总线)"),
    (520,273, "PB1  → VS1838B IR_OUT (EXTI)"),
    (520,290, "PB2  → TIM3_CH3 红外发射PWM"),
    (520,307, "PB6  → I2C1_SCL (BH1750+OLED)"),
    (520,324, "PB7  → I2C1_SDA (BH1750+OLED)"),
    (520,341, "PC0  → 继电器1 IN (灯光)"),
    (520,358, "PC1  → 继电器2 IN (风扇)"),
    (520,375, "PC2  → 继电器3 IN (空调)"),
    (520,392, "PC3  → 继电器4 IN (插座)"),
    (520,409, "NRST → 复位按键+10kΩ上拉"),
    (520,426, "OSC_IN/OUT → 8MHz+22pF×2"),
    (520,443, "VDD/VSS → 3.3V + 100nF去耦×6"),
    (520,460, "VDDA → 3.3V + 10uF+100nF"),
]
for x,y,txt in mcu_pins_desc:
    add_text(x,y, txt, 10)

# MCU电源去耦标注
add_text(760,120, "C6-C11: 100nF×6 (VDD去耦)", 10)
add_text(760,140, "C12: 10uF + C13: 100nF (VDDA)", 10)

# 晶振
add_text(760,170, "Y1: 8MHz CSTCE8M00G52-R0", 10)
add_text(760,187, "C14: 22pF  C15: 22pF", 10)

# 复位
add_text(760,217, "R1: 10kΩ NRST上拉", 10)
add_text(760,234, "SW1: 复位按键 → GND", 10)

# MCU区域的网络标签
mcu_nets = [
    (510,120,"KEY1"), (510,137,"KEY2"),
    (510,154,"ESP_RXD"), (510,171,"ESP_TXD"),
    (510,256,"DHT11_DATA"), (510,273,"IR_IN"), (510,290,"IR_PWM"),
    (510,307,"I2C_SCL"), (510,324,"I2C_SDA"),
    (510,341,"RELAY1"), (510,358,"RELAY2"), (510,375,"RELAY3"), (510,392,"RELAY4"),
]
for x,y,net in mcu_nets:
    add_net(x,y,net)

# ==================== 3. 传感器 ====================
add_rect(80,480,400,310, "#10b981", "rgba(16,185,129,0.03)")
add_text(100,490, "传感器模块 Sensors", 14, "Comment")

# DHT11 温湿度
add_rect(100,510,160,110, "#10b981")
add_text(120,520, "DHT11 温湿度传感器", 12, "Comment")
add_text(120,540, "VDD → 3.3V", 10)
add_text(120,555, "DATA → PB0", 10)
add_text(120,570, "GND → GND", 10)
add_text(120,590, "R2: 4.7kΩ DATA上拉", 10)
add_net(120,600, "DHT11_DATA")

# BH1750 光照
add_rect(300,510,160,120, "#8b5cf6")
add_text(315,520, "BH1750 光照传感器", 12, "Comment")
add_text(315,540, "VCC → 3.3V", 10)
add_text(315,555, "SCL → PB6 (I2C)", 10)
add_text(315,570, "SDA → PB7 (I2C)", 10)
add_text(315,585, "ADDR → GND (0x23)", 10)
add_text(315,600, "R3=R4: 4.7kΩ I2C上拉", 10)
add_net(300,615, "I2C_SCL")
add_net(300,630, "I2C_SDA")

# OLED 显示
add_rect(100,640,240,120, "#3b82f6", "rgba(59,130,246,0.03)")
add_text(120,650, "OLED 0.96\" 128×64 显示屏", 12, "Comment")
add_text(120,670, "VCC → 3.3V", 10)
add_text(120,685, "SCL → PB6 (I2C)  地址:0x3C")
add_text(120,700, "SDA → PB7 (I2C)")
add_text(120,715, "GND → GND")
add_text(120,735, "C16: 100nF VCC去耦", 10)

# ==================== 4. WiFi模块 ====================
add_rect(1200,80,260,220, "#06b6d4", "rgba(6,182,212,0.03)")
add_text(1220,90, "WiFi 通信模块", 14, "Comment")

add_rect(1220,115,220,140, "#06b6d4")
add_text(1240,125, "ESP8266-01S", 12, "Comment")
add_text(1240,143, "VCC  → 3.3V (≥500mA)", 10)
add_text(1240,158, "RXD  → PA2 (STM32 TX)", 10)
add_text(1240,173, "TXD  → PA3 (STM32 RX)", 10)
add_text(1240,188, "CH_PD → 3.3V (R5:10k)", 10)
add_text(1240,203, "RST  → 3.3V (R6:10k)", 10)
add_text(1240,218, "GPIO0 → SW2按键 (下载模式)", 10)
add_text(1240,235, "C17: 100uF + C18: 100nF 去耦", 10)

add_net(1460,158, "ESP_RXD")
add_net(1460,173, "ESP_TXD")

# ==================== 5. 红外模块 ====================
add_rect(1200,320,260,160, "#f97316", "rgba(249,115,22,0.03)")
add_text(1220,330, "红外遥控模块", 14, "Comment")

add_rect(1220,355,240,80, "#f97316")
add_text(1240,365, "VS1838B 红外接收头", 12, "Comment")
add_text(1240,383, "VCC → 3.3V   OUT → PB1", 10)
add_text(1240,398, "GND → GND", 10)
add_text(1240,420, "IR_LED: 红外发射管 + 47Ω → PB2(PWM 38kHz)", 10)
add_net(1460,383, "IR_IN")
add_net(1460,420, "IR_PWM")

# ==================== 6. 调试接口 ====================
add_rect(1200,500,260,140, "#64748b", "rgba(100,116,139,0.03)")
add_text(1220,510, "SWD 调试接口", 14, "Comment")
add_text(1220,530, "SWDIO → PA13   SWCLK → PA14", 10)
add_text(1220,548, "VCC → 3.3V   GND → GND", 10)
add_text(1220,566, "NRST → NRST (可选)", 10)
add_text(1220,610, "USB→UART: CH340G (预留调试串口)", 11, "Comment")
add_text(1220,628, "PA9(TX) → CH340 RX | PA10(RX) → CH340 TX", 10)

# ==================== 7. 4路继电器 ====================
add_rect(80,800,700,250, "#dc2626", "rgba(220,38,38,0.03)")
add_text(100,810, "执行模块 - 4路继电器控制", 14, "Comment")

relay_info = [
    ("RELAY1", "PC0", "Q2:S8050", "RL1:SRD-05VDC", "灯光控制"),
    ("RELAY2", "PC1", "Q3:S8050", "RL2:SRD-05VDC", "风扇控制"),
    ("RELAY3", "PC2", "Q4:S8050", "RL3:SRD-05VDC", "空调/插座"),
    ("RELAY4", "PC3", "Q5:S8050", "RL4:SRD-05VDC", "备用"),
]
for i,(net,stm32,transistor,relay,usage) in enumerate(relay_info):
    y = 840 + i*40
    add_net(80, y, net)
    add_text(100, y, f"{stm32} → {transistor} → {relay} (续流1N4007) → {usage}", 10)

add_text(100, 1020, "继电器电源: 5V 独立电源 (与MCU 3.3V隔离)", 10)
add_text(100, 1037, "续流二极管: 1N4007 ×4 (反并联在继电器线圈两端)", 10)

# ==================== 8. 本地控制 ====================
add_rect(1200,660,260,180, "#f59e0b", "rgba(245,158,11,0.03)")
add_text(1220,670, "本地控制", 14, "Comment")
add_text(1220,690, "KEY1 (PA0) : 模式切换", 10)
add_text(1220,708, "      10kΩ上拉→3.3V, 按键→GND", 10)
add_text(1220,730, "KEY2 (PA1) : 确认/开关", 10)
add_text(1220,748, "      10kΩ上拉→3.3V, 按键→GND", 10)
add_text(1220,770, "LED1: 3.3V→220Ω→LED→GND (电源指示)", 10)
add_text(1220,788, "LED2: PB1→220Ω→LED→GND (状态指示)", 10)
add_text(1220,810, "R7:220Ω  R8:220Ω (限流电阻)", 10)

# ==================== 9. 去耦电容汇总 ====================
add_rect(80,1080,500,160, "#64748b", "rgba(100,116,139,0.03)")
add_text(100,1090, "去耦电容清单", 14, "Comment")
caps = [
    "C1: 10uF  AMS1117 输入", "C2: 100nF AMS1117 输入",
    "C3: 10uF  AMS1117 输出", "C4: 100nF AMS1117 输出",
    "C5: 100uF AMS1117 输入(电解)", "C6-C11: 100nF×6 STM32 VDD各引脚",
    "C12: 10uF VDDA滤波", "C13: 100nF VDDA高频",
    "C14: 22pF  8MHz晶振", "C15: 22pF  8MHz晶振",
    "C16: 100nF OLED VCC", "C17: 100uF ESP8266供电",
    "C18: 100nF ESP8266高频",
]
for i, cap in enumerate(caps):
    add_text(100, 1110 + i*16, cap, 10)

# ==================== 10. 网络汇总 ====================
add_text(600, 1090, "网络连接总线", 14)
add_text(600, 1115, "3.3V 网络: STM32(VDD/VDDA) + ESP8266 + DHT11 + BH1750 + OLED + 红外", 10)
add_text(600, 1135, "GND 网络: 所有模块共地, 单点接地", 10)
add_text(600, 1155, "I2C总线: SCL(PB6) → BH1750 SCL + OLED SCL (4.7kΩ上拉×2)", 10)
add_text(600, 1175, "I2C总线: SDA(PB7) → BH1750 SDA + OLED SDA (4.7kΩ上拉×2)", 10)
add_text(600, 1195, "UART1(PA9/PA10): 调试串口(CH340G)", 10)
add_text(600, 1215, "UART2(PA2/PA3): ESP8266 通信 (115200 8N1)", 10)

# ==================== 网络标签：电源 ====================
add_net(160, 90, "12V_IN")
add_net(360, 90, "3.3V")
add_net(160, 430, "GND")
add_net(360, 430, "GND")

# =============== 构建完整JSON ===============
schematic = [{
    "head": {
        "docType": "3",
        "editorVersion": "6.4.43",
        "newgId": True,
        "c_para": {"ischeck": True, "sim_step": "0.01", "sim_mode": "time domain"},
        "x": 0, "y": 0, "id": ""
    },
    "canvas": {
        "BOUNDARY": {"x": 0, "y": 0, "width": W+40, "height": H+40},
        "GRID": {"step": 10, "size": 10, "dotted": False, "color": "#CCCCCC"},
        "width": W+40, "height": H+40
    },
    "shape": shapes,
    "element": elements
}]

os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
with open(OUTPUT, 'w', encoding='utf-8') as f:
    json.dump(schematic, f, indent=2, ensure_ascii=False)

size_kb = os.path.getsize(OUTPUT)/1024
print("OK - 原理图已生成: " + OUTPUT)
print("   元件数: " + str(len(elements)) + "  |  图形/标注: " + str(len(shapes)))
print("   文件大小: " + str(round(size_kb,1)) + " KB")
print("")
print("使用方式:")
print("   1. 打开 嘉立创EDA (LCEDA)")
print("   2. 文件 -> 打开 -> 选择 " + OUTPUT)
print("   3. 可在基础上添加实际库元件并布线")
