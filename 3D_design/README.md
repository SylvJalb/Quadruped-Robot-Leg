# Print informations

Brand: [Creality](https://www.creality3dofficial.com/)  
Model: [Ender 3 Pro](https://www.creality3dofficial.com/products/creality-ender-3-pro-3d-printer/)      
Filament size: 1.75mm       


## **Leg**
### > PLA
Use PLA Generic default settings in Cura, and change :
- Wall thickness: 4mm   
<!--- - Deactivate "Mesh Fixes" > "Union Overlapping Volumes" -->

| Part | Nozzle Size | Thickness | Infill | Support | Adhesion | Weight |
|:----|:------:|:-------:|------:|:-------:|:------:|------:|
| arm_case_lid | 0.8 | 0.32 | 50% | No | No | 54g |
| arm_case_part1 | 0.8 | 0.32 | 30% | 51° | No | 197g |
| arm_case_part2 | 0.8 | 0.32 | 50% | 51° | No | 192g |
| arm_holder | 0.8 | 0.32 | 50% | 51° | No | 304g |
| arm_separator | 0.8 | 0.32 | 40% | No | No | 30g |
| foot_holder_part1 | 0.4 | 0.2 | 50% | 35° | No | 23g |
| foot_holder_part2 | 0.4 | 0.2 | 50% | 35° | No | 22g |
| forearm_holder | 0.4 | 0.2 | 50% | 35° | No | 100g |
| forearm_gear_arm | 0.4 | 0.16 | 60% | No | No | 50g |
| forearm_gear_knee | 0.4 | 0.16 | 30% | No | No | 28g |
| forearm_separators (1&2) | 0.4 | 0.32 | 100% | No | No | 3g |
| shoulder_case | 0.8 | 0.32 | 50% | 51° | Yes | 564g |
| shoulder_holder_back | 0.8 | 0.32 | 30% | 51° | No | 282g |
| shoulder_holder_front | 0.8 | 0.32 | 30% | No | No | 107g |
| shoulder_separator | 0.8 | 0.32 | 40% | No | No | 30g |

### > TPU 95A
Use TPU 95A Generic default settings in Cura, and change :
- nozzle size: 0.4mm
- Layer height: 0.12mm
- Infill: 20%
- Infill pattern: Cubic Subdivision
- Infill line multiplier: 3
- Wall thickness: 1.5mm
- Printing temperature: 228°C
- Build plate temperature: None

foot_ball -> 31g

## **OpenTorque Actuator**
You have to print 3 actuators. The first one is the one that is connected to the shoulder. The second one is the one that is connected to the arm. The third one is the one that is connected to the forearm. There are all three the same.

**This is instructions to print only one actuator :**

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
| planet_carrier_2_acisre | 60% | 35° | 45g |
| planet_carrier_acisre | 100% | 35° | 68g |

### > Nylon
Use PLA Generic default settings in Cura, and change :
- nozzle size: 0.4mm
- Layer height: 0.2mm
- Wall thickness: 0.8mm
- Printing temperature: 260°C
- Build plate temperature: 70°C
- Printing speed: 35mm/s
- Retraction distance: 1.5mm
- Minimum extrusion distance window: 3mm
- No Adhesion plate
- Disable Print Cooling

| Part | Infill | Support | Weight for 1 | Quantity |
|:-----|:------:|:------:|:------:|:--------:|
| actuator_housing_acisre | 70% | 60° | 110g | 1 |
| planet_gear_acisre | 70% | no | 12g | 3 |
| sun_gear_acisre | 60% | no | 15g | 1 |
