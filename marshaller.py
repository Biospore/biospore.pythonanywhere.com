#!/usr/bin/python3

import xml.etree.ElementTree as ET

class Storage:
    counter = 0
    ip_set = set()
    def __init__(self, obj=None):
        self.counter = 0
        self.ip_set = set()
        if obj:
            self.unmarshal(obj)

    def add_ip(self, ip):
        self.ip_set.add(ip)
        self.counter = len(self.ip_set)
        return True

    def get_counter(self):
        return self.counter

    def marshal(self):
        # Marshal current object state to string(in xml format)
        storage = ET.Element('storage')
        ET.SubElement(storage, 'counter').text = str(self.counter)
        ips = ET.SubElement(storage, 'ips')
        for ip in self.ip_set:
            ET.SubElement(ips, 'ip').text = ip
        return ET.tostring(storage).decode()

    def unmarshal(self, obj):
        # Gets the filename as 'obj', parse it and updates self values
        tree = ET.parse(obj)
        storage = tree.getroot()
        for child in storage:
            if child.tag == 'counter':
                self.counter = int(child.text)
            if child.tag == 'ips':
                self.ip_set = set()
                for ip in child:
                    self.ip_set.add(ip.text)
        return True

class Storage2:
    comments = []
    def __init__(self, obj=None):
        self.comments = []
        if obj:
            self.unmarshal(obj)

    def add_comment(self, name, email, text):
        if (name, email, text) not in self.comments:
            self.comments.append((name, email, text))
        return True

    def get_comments(self):
        return self.comments

    def marshal(self):
        # Marshal current object state to string(in xml format)
        storage = ET.Element('storage')
        for node in self.comments:
            tnode = ET.SubElement(storage, 'node')
            ET.SubElement(tnode, 'name').text = node[0]
            ET.SubElement(tnode, 'email').text = node[1]
            ET.SubElement(tnode, 'text').text = node[2]
        return "<?xml version='1.0' encoding='utf-8'?>" + ET.tostring(storage).decode()

    def unmarshal(self, obj):
        # Gets the filename as 'obj', parse it and updates self values
        tree = ET.parse(obj)
        storage = tree.getroot()
        for child in storage:
            if child.tag == 'node':
                name = ''
                email = ''
                text = ''
                for nchild in child:
                    if nchild.tag == 'name':
                        name = nchild.text
                    if nchild.tag == 'email':
                        email = nchild.text
                    if nchild.tag == 'text':
                        text = nchild.text
                self.comments.append((name, email, text))
        return True


class Storage3:
    images = []
    def add_image(self, path, thumb):
        self.images.append(Img(0, path, thumb))

    def liked(self, path, fromwho):
        for i in self.images:
            if i.path == path:
                if fromwho in i.fromwho:
                    i.likes -= 1
                    i.fromwho.remove(fromwho)
                else:
                    i.likes += 1
                    i.fromwho.append(fromwho)

    def get_all_images(self):
        imgs = []
        for i in self.images:
            imgs.append((i.path, i.thumb, i.likes))
        return imgs

    def marshal(self):
        storage = ET.Element('storage')
        for image in self.images:
            tnode = ET.SubElement(storage, 'image')
            tnode.set('path', image.path)
            tnode.set('thumb', image.thumb)
            tnode.set('likes', str(image.likes))
            tnode.set('from', str(image.fromwho))
        return "<?xml version='1.0' encoding='utf-8'?>" + ET.tostring(storage).decode()

    def unmarshal(self, obj):
        tree = ET.parse(obj)
        storage = tree.getroot()
        for child in storage:
            img = Img(int(child.attrib['likes']), child.attrib['path'], child.attrib['thumb'])
            img.fromwho = eval(child.attrib['from'])
            self.images.append(img)
        return True

class Img:
    likes = 0
    path = ''
    thumb = ''
    fromwho = []
    def __init__(self, l, p, t):
        self.likes = l
        self.path = p
        self.thumb = t

#a = Storage()
#c = Storage()
#a.add_ip("127.0.0.1")
#a.add_ip("127.0.0.2")
#a.add_ip("127.0.0.3")
#a.add_ip("127.0.0.4")

#b = a.marshal()
#c.unmarshal('marshalled.xml')
