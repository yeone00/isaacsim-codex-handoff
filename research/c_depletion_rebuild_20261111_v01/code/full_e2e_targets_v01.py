import math
from evaluation.full_e2e_contract_v01 import exact,finite

def generate(predicted_center,task):
    exact(predicted_center,['center_x_m','center_y_m']);exact(task,['task_yaw_deg','designated_face'])
    x=finite(predicted_center['center_x_m']);y=finite(predicted_center['center_y_m']);yaw=finite(task['task_yaw_deg'])
    if task['designated_face']!='local_-X':raise ValueError('Locked designated face required')
    th=math.radians(yaw);nx,ny=-math.cos(th),-math.sin(th)
    return {'yaw_deg':yaw,'pre_x_m':x+2.203745031260775*nx,'pre_y_m':y+2.203745031260775*ny,'final_x_m':x+1.403745031260775*nx,'final_y_m':y+1.403745031260775*ny}

def evaluate_terminal(terminal,canonical_final,controller_errors):
    # Evaluation-only function; never called to choose masks or controller targets.
    exact(terminal,['x_m','y_m','yaw_deg']);exact(canonical_final,['x_m','y_m','yaw_deg'])
    exact(controller_errors,['long_m','lat_m','yaw_deg'])
    for d in [terminal,canonical_final,controller_errors]:
        for v in d.values():finite(v)
    error=math.hypot(terminal['x_m']-canonical_final['x_m'],terminal['y_m']-canonical_final['y_m'])
    angle=abs((terminal['yaw_deg']-canonical_final['yaw_deg']+180)%360-180)
    qc=abs(controller_errors['long_m'])<=.03 and abs(controller_errors['lat_m'])<=.03 and abs(controller_errors['yaw_deg'])<=2
    bands={'strict':(.055,3.686017625614643),'main':(.11,7.34177432289679),'relaxed':(.165,10.9384737479652)}
    return {'engineering_controller_qc':qc,'research_task_success':{k:error<=p and angle<=a for k,(p,a) in bands.items()},'canonical_2d_error_m':error,'facing_error_deg':angle}
