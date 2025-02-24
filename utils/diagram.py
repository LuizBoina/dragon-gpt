import json

class DiagramHandler():
  flow_type = "flow"
  actor_type = "actor"
  process_type = "process"
  store_type = "store"
  trust_boundary_curve_type = "trust-broundary-curve"
  trust_boundary_box_type = "trust-boundary-box"
  def __init__(self, filename):
    self.filename = filename
    self.diagram_type = ""
    self.components = []
    self.component_sentence_handler_map = {
      DiagramHandler.flow_type: self.make_flow_sentence,
      DiagramHandler.actor_type: self.make_actor_sentence,
      DiagramHandler.process_type: self.make_process_sentence,
      DiagramHandler.store_type: self.make_store_sentence,
      DiagramHandler.trust_boundary_curve_type: self.make_trust_boundary_sentence,
      DiagramHandler.trust_boundary_box_type: self.make_trust_boundary_sentence,
    }

  def read_data(self):
    with open(self.filename, "r") as f:
      data = json.load(f)
      # Consider only the first diagram of the file
      diagram = data["detail"]["diagrams"][0]
      self.diagram_type = diagram["diagramType"]
      for comp in diagram["cells"]:
        if not (comp["shape"] == DiagramHandler.trust_boundary_box_type 
          or comp["shape"] == DiagramHandler.trust_boundary_curve_type) and comp["data"]["outOfScope"]:
          continue
        new_comp = {
          "id": comp["id"],
          "type": comp["shape"],
          "name": comp["data"]["name"],
          "description": comp["data"]["description"],
        }
        # if component is a trust boundary, add vertices
        if new_comp["type"] == DiagramHandler.trust_boundary_curve_type:
          new_comp["vertices"] = [ comp["source"] ]
          for point in comp["vertices"]:
            new_comp["vertices"].append(point)
          new_comp["vertices"].append(comp["target"])
        elif new_comp["type"] == DiagramHandler.flow_type:
          new_comp["source"] = comp["source"]["cell"]
          new_comp["target"] = comp["target"]["cell"]
          new_comp["isBidirectional"] = comp["data"].get("isBidirectional", False)
          new_comp["isEncrypted"] = comp["data"]["isEncrypted"]
          new_comp["protocol"] = comp["data"]["protocol"]
          new_comp["isPublicNetwork"] = comp["data"]["isPublicNetwork"]
        else:
          new_comp["position"] = comp["position"]
          if new_comp["type"] == DiagramHandler.trust_boundary_box_type:
            new_comp["size"] = comp["size"]
          else:
            new_comp["flow"] = []
            if new_comp["type"] == DiagramHandler.actor_type:
              new_comp["providesAuthentication"] = comp["data"]["providesAuthentication"]
            elif new_comp["type"] == DiagramHandler.store_type:
              new_comp["isALog"] = comp["data"]["isALog"]
              new_comp["storesCredentials"] = comp["data"]["storesCredentials"]
              new_comp["isEncrypted"] = comp["data"]["isEncrypted"]
              new_comp["isSigned"] = comp["data"]["isSigned"]
        self.components.append(new_comp)
    
  def make_flow_sentence(self, flow_arr):
    sentence = ""
    for idx, flow in enumerate(flow_arr):
      if idx > 0:
        sentence += ". It also "
      way = "bidirectional" if flow["isBidirectional"] else "directional"
      name = flow["name"]
      if flow["description"] != "":
        name += ", described as {}, ".format(flow["description"])
      if flow["protocol"] != "":
        name += "({} protocol)".format(flow["protocol"])
      encrypted_text = "encrypted" if flow["isEncrypted"] else "not encrypted"
      network_text = "public" if flow["isPublicNetwork"] else "private"
      sentence += " interacts in a {} way with the \"{}\" by doing a {}, which is {} in a {} network".format(
        way, flow["target_name"], name, encrypted_text, network_text)
    return sentence
    

  def intro_sentence(self, comp):
    sentence = "The \"{}\"".format(comp["name"])
    if comp["description"] != "":
      sentence += ", described as {}".format(comp["description"])
    return sentence
  
  def format_sentence(self, sentence):
    return sentence.replace("\n", "") + ";\n"

  def make_actor_sentence(self, comp):
    sentence = self.intro_sentence(comp)
    if comp["providesAuthentication"]:
        sentence += ", which doesn't need to authenticate."
        # Add preventive measures
        sentence += " To enhance security, consider implementing authentication mechanisms."
    else:
      sentence += ", which needs to authenticate."
    sentence += self.make_flow_sentence(comp["flow"])
    return self.format_sentence(sentence)



  def make_process_sentence(self, comp):
    sentence = self.intro_sentence(comp)
    sentence += self.make_flow_sentence(comp["flow"])
    
    return self.format_sentence(sentence)
    

  def make_store_sentence(self, comp):
    sentence = self.intro_sentence(comp)
    used_for, state = [], []
    if comp["isALog"]:
      used_for.append("log data")
    if comp["storesCredentials"]:
      used_for.append("store credentials")
    if comp["isEncrypted"]:
      state.append("encrypted")
    if comp["isSigned"]:
      state.append("signed")
    if len(used_for):
      sentence += ", which is used to {}".format(" and ".join(used_for))
    if len(state):
      if len(used_for):
        sentence += " and is {},".format(" and ".join(state))
      else:
        sentence += ", which is {},".format(" and ".join(state))
    if len(used_for) and not len(used_for):
      sentence += ","
    sentence += self.make_flow_sentence(comp["flow"])
    return self.format_sentence(sentence)
    
  

  # assume that everything that is on the rigth of the curve is inside of trust boundary
  def make_trust_boundary_sentence(self, comp):
    sentence = self.intro_sentence(comp)
    outside, inside = [], []
    for _comp in self.components:
      # this kind of component was sorted to be in the end of array
      if _comp["type"] == DiagramHandler.trust_boundary_box_type or _comp["type"] == DiagramHandler.trust_boundary_curve_type:
        break
      is_outside = False
      if comp["type"] == DiagramHandler.trust_boundary_curve_type:
        is_outside = self.is_outside_of_tb_curve(_comp["position"], comp["vertices"])
      else:
        is_outside = self.is_outside_of_tb_box(_comp["position"], comp["position"], comp["size"])
      if is_outside:
        outside.append(_comp["name"])
      else:
        inside.append(_comp["name"])
    format_comps = lambda x: " and ".join(map(lambda y: f"\"{y}\"".replace("\n", ""), x))
    outside, inside = format_comps(outside), format_comps(inside)
    sentence += " is a trust boundary that separate {} (outside of trust zone) from {} (inside of trust zone)".format(outside, inside)
    return self.format_sentence(sentence)
    

  def make_component_sentence(self, idx):
    comp = self.components[idx]
    component_type = comp["type"]
    if component_type in self.component_sentence_handler_map:
      return self.component_sentence_handler_map[component_type](comp)
    else:
      print(f"Invalid type: {component_type}")
      exit()
  
  # prevent of flow and tb going before the components that it's connects/separe
  def sort_components(self):
    def flow_and_tb_in_the_end(obj):
      if obj["type"] == DiagramHandler.actor_type:
        return 0
      elif obj["type"] == DiagramHandler.process_type:
        return 1
      elif obj["type"] == DiagramHandler.store_type:
        return 2
      elif obj["type"] == DiagramHandler.trust_boundary_curve_type or obj["type"] == DiagramHandler.trust_boundary_box_type:
        return 3
      elif obj["type"] == DiagramHandler.flow_type:
        return 4
      return -1
    
    self.components = sorted(self.components, key=flow_and_tb_in_the_end)

  def get_target_name_by_id(self, target_id):
    for comp in self.components:
      if comp["id"] == target_id:
        return comp["name"]


  def add_flow_to_the_component(self, flow):
    for comp in self.components:
      if comp["id"] == flow["source"]:
        flow["target_name"] = self.get_target_name_by_id(flow["target"])
        comp["flow"].append(flow)
        break

  def add_flow_to_the_components(self):
    # find the first occurrence of flow component in array
    first_flow_occ = -1
    for idx, comp in enumerate(self.components):
      if comp["type"] == DiagramHandler.flow_type:
        first_flow_occ = idx
        break
    # remove the flow components from components array
    flow_arr = self.components[first_flow_occ:]
    self.components = self.components[:first_flow_occ]
    for flow_comp in flow_arr:
      self.add_flow_to_the_component(flow_comp)
        
  def make_sentence(self):
    self.read_data()

    self.sort_components()
    self.add_flow_to_the_components()
    introduction = "I will describe the components of a software architecture and I need your help to do the threat modeling of this scenario.\nThe components are these:\n"
    comp_sentences = []
    for idx in range(len(self.components)):
      c_sentence = self.make_component_sentence(idx)
      topic_sentence = f"{idx + 1}. {c_sentence}"
      comp_sentences.append(topic_sentence)
    last_sentence = f"Based on the given scenario, generate a list of threats and categorize each threat using the {self.diagram_type} model."
    return introduction + "".join(comp_sentences) + last_sentence
  

  def is_outside_of_tb_box(self, comp, box, size):
    if comp["x"] >= box["x"] and comp["x"] <= box["x"] + size["width"] and comp["y"] >= box["y"] and comp["y"] <= box["y"] + size["height"]:
        return True
    else:
        return False

  # use cross product to determine if the component is on the left (outside) or on the right (inside) of the trust boundary curve
  def is_outside_of_tb_curve(self, comp_position, vertices):
    def cross_product(v1, v2):
        return v1[0] * v2[1] - v1[1] * v2[0]

    is_right = 0  # Initialize to zero

    for i in range(len(vertices) - 1):
        v1 = (vertices[i]["x"] - comp_position["x"], vertices[i]["y"] - comp_position["y"])
        v2 = (vertices[i + 1]["x"] - comp_position["x"], vertices[i + 1]["y"] - comp_position["y"])
        cross = cross_product(v1, v2)

        # Point lies on the curve, so it's on the right
        if cross >= 0:
            is_right += 1
        else:
            is_right -= 1

    # Check the last vertex and the first vertex (loop closing)
    v1 = (vertices[-1]["x"] - comp_position["x"], vertices[-1]["y"] - comp_position["y"])
    v2 = (vertices[0]["x"] - comp_position["x"], vertices[0]["y"] - comp_position["y"])
    cross = cross_product(v1, v2)

    # Point lies on the curve, so it's on the right
    if cross := 0:
        is_right += 1
    else:
        is_right -= 1

    if is_right == len(vertices) or is_right == -len(vertices):
        return False  # Point lies on the curve
    return is_right > 0