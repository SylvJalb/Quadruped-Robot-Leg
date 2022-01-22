🚨 All this instructions are not been tested yet.

# Print informations

Brand: [Creality](https://www.creality3dofficial.com/)  
Model: [Ender 3 Pro](https://www.creality3dofficial.com/products/creality-ender-3-pro-3d-printer/)      
Filament size: 1.75mm       


## **Leg**
### > PLA
Use PLA Generic default settings in Cura, and change :
- Wall thickness: 4mm   
- Deactivate "Mesh Fixes" > "Union Overlapping Volumes"

| Part | Nozzle Size | Thickness | Infill | Support | Adhesion | Weight |
|:----|:------:|:-------:|------:|:-------:|:------:|------:|
| arm_case_lid | 0.8 | 0.32 | 30% | No | No | 74g |
| arm_case_part1 | 0.8 | 0.32 | 30% | 35° | No | 371g |
| arm_case_part2 | 0.8 | 0.32 | 50% | 35° | No | 281g |
| arm_holder | 0.8 | 0.32 | 30% | 35° | No | 369g |
| arm_separator | 0.8 | 0.32 |  | No | No |  |
| foot_holder_part1 | 0.4 | 0.2 | 50% | 35° | No | 21g |
| foot_holder_part2 | 0.4 | 0.2 | 50% | 35° | No | 21g |
| forearm_holder | 0.4 | 0.2 | 50% | 35° | No | 100g |
| shoulder_case | 0.8 | 0.32 | 50% | 35° | Yes | 576g |
| shoulder_holder_back | 0.8 | 0.32 | 30% | 35° | No | 354g |
| shoulder_holder_front | 0.8 | 0.32 | 30% | No | No | 146g |
| shoulder_separator | 0.8 | 0.32 | 100% | No | No | 40g |

### > Nylon
Use PLA Generic default settings in Cura, and change :
- nozzle size: 0.4mm
- Layer height: 0.2mm
- Wall thickness: 0.8mm
- Printing temperature: 250°C
- Build plate temperature: 100°C
- Printing speed: 35mm/s
- Retraction distance: 1.5mm
- Minimum extrusion distance window: 3mm
- No Adhesion plate
- Disable Print Cooling
- No support

| Part | Infill | Weight |
|:-----|:------:|:------:|
| forearm_gear_arm | 30% |  |
| forearm_gear_knee | 30% |  |

## **OpenTorque Actuator**
You have to print 3 actuators. The first one is the one that is connected to the shoulder. The second one is the one that is connected to the arm. The third one is the one that is connected to the forearm. There are all three the same.

This is instructions to print only one actuator :

### > PLA
Use PLA Generic default settings in Cura, and change :
- Wall thickness: 2.4mm
- nozzle size: 0.4mm
- Layer height: 0.28mm
- No Adhesion plate

| Part | Infill | Support | Weight |
|:-----|:------:|:-------:|:------:|
| actuator_housing_2_acisre | 50% | 50° | 142g |
| backplate_acisre | 50% | No | 41g |
| encoder_cover_acisre | 20% | No | 11g |
| front_clamp_ring_acisre | 50% | No | 14g |
| magnet_holder | 30% | No | 2g |
| planet_carrier_2_acisre | 50% | 35° | 41g |
| planet_carrier_acisre | 50% | 35° | 68g |

### > Nylon
Use PLA Generic default settings in Cura, and change :
- nozzle size: 0.4mm
- Layer height: 0.2mm
- Wall thickness: 0.8mm
- Printing temperature: 250°C
- Build plate temperature: 100°C
- Printing speed: 35mm/s
- Retraction distance: 1.5mm
- Minimum extrusion distance window: 3mm
- No Adhesion plate
- Disable Print Cooling

| Part | Infill | Support | Weight for 1 | Quantity |
|:-----|:------:|:------:|:------:|:--------:|
| actuator_housing_acisre | 40% | 60° | 85g | 1 |
| planet_gear_acisre | 50% | no | 10g | 3 |
| sun_gear_acisre | 50% | no | 13g | 1 |