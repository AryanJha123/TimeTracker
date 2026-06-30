import bpy
import time
from datetime import datetime, timedelta
import rna_keymap_ui
from bpy.utils import register_class, unregister_class

bl_info = {
    "name" : "TimeTracker",  
    "category": "3D View",   
    "author": "AryanJha123",
    "blender": (3, 4, 1),
    "version": (0, 0, 1),
    "description": "Track time.",
    "doc_url": "",
    "tracker_url": "",
}

class TimeCheck(bpy.types.Operator):
    bl_idname = "input.time_check"
    bl_label = "TimeCheck"
    def execute(self, context):
        scene = context.scene
        now = datetime.now().timestamp()

        if "target" not in scene:
            scene["target"] = now
            scene["time"] = 0.0
            return {'FINISHED'}
        elapsed = now - scene["target"]

        if elapsed < 20:
            scene["time"] = scene.get("time", 0.0) + elapsed
        scene["target"] = now

        total = int(scene.get("time", 0))
        context.workspace.status_text_set(f"Time: {total // 3600}:{(total // 60) % 60:02d}:{total % 60:02d}")

        return {'FINISHED'}

keys = {"MENU": [{"label": "Timer",
                  "region_type": "WINDOW",
                  "space_type": "EMPTY",
                  "map_type": "MOUSE_BUTTON",
                  "keymap": "Window",
                  "idname": "input.time_check",
                  "type": "LEFTMOUSE",
                  "ctrl": False,
                  "alt": False,
                  "shift": False,
                  "oskey": False,
                  "value": "CLICK"
                  },
                  {"label": "Timer",
                  "region_type": "WINDOW",
                  "space_type": "EMPTY",
                  "map_type": "MOUSE_BUTTON",
                  "keymap": "Window",
                  "idname": "input.time_check",
                  "type": "RIGHTMOUSE",
                  "ctrl": False,
                  "alt": False,
                  "shift": False,
                  "oskey": False,
                  "value": "ANY"
                  },
                  {"label": "Timer",
                  "region_type": "WINDOW",
                  "space_type": "EMPTY",
                  "map_type": "MOUSE_BUTTON",
                  "keymap": "Window",
                  "idname": "input.time_check",
                  "type": "BUTTON4MOUSE",
                  "ctrl": False,
                  "alt": False,
                  "shift": False,
                  "oskey": False,
                  "value": "ANY"
                  },
                  {"label": "Timer",
                  "region_type": "WINDOW",
                  "space_type": "EMPTY",
                  "map_type": "MOUSE_BUTTON",
                  "keymap": "Window",
                  "idname": "input.time_check",
                  "type": "BUTTON5MOUSE",
                  "ctrl": False,
                  "alt": False,
                  "shift": False,
                  "oskey": False,
                  "value": "ANY"
                  },
                  {"label": "Timer",
                  "region_type": "WINDOW",
                  "space_type": "EMPTY",
                  "map_type": "MOUSE_BUTTON",
                  "keymap": "Window",
                  "idname": "input.time_check",
                  "type": "MIDDLEMOUSE",
                  "ctrl": False,
                  "alt": False,
                  "shift": False,
                  "oskey": False,
                  "value": "ANY"
                  },
                  ]}

def get_keys():
    keylists = []
    keylists.append(keys["MENU"])
    return keylists

def register_keymaps(keylists):
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    keymaps = []

    for keylist in keylists:
        for item in keylist:
            keymap = item.get("keymap")
            space_type = item.get("space_type", "EMPTY")
            region_type = item.get("region_type", "WINDOW")

            if keymap:
                km = kc.keymaps.new(name=keymap, space_type=space_type, region_type=region_type)
                # km = kc.keymaps.new(name=keymap, space_type=space_type)

                if km:
                    idname = item.get("idname")
                    type = item.get("type")
                    value = item.get("value")

                    shift = item.get("shift", False)
                    ctrl = item.get("ctrl", False)
                    alt = item.get("alt", False)
                    oskey = item.get("oskey", False)

                    kmi = km.keymap_items.new(idname, type, value, shift=shift, ctrl=ctrl, alt=alt, oskey=oskey)

                    if kmi:
                        properties = item.get("properties")

                        if properties:
                            for name, value in properties:
                                setattr(kmi.properties, name, value)

                        keymaps.append((km, kmi))
    return keymaps

def unregister_keymaps(keymaps):
    for km, kmi in keymaps:
        km.keymap_items.remove(kmi)

def draw(self, context):
    scene = context.scene
    vl = context.view_layer
    self.layout.label(text=scene.statistics(vl))

def register():
    register_class(TimeCheck)
    global keymaps
    keys = get_keys()
    keymaps = register_keymaps(keys)

def unregister():
    global keymaps
    for km, kmi in keymaps:
        km.keymap_items.remove(kmi)
    unregister_class(TimeCheck)
    
if __name__ == "__main__":
    register()