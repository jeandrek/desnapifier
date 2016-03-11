# Copyright (C) 2016 Jeandre Kruger
#
# This file is part of screchifier.
#
# screchifier is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# screchifier is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with screchifier.  If not, see <http://www.gnu.org/licenses/>.

import kurt, sys
import xml.etree.ElementTree
import notsupported, sprites, scripts

if len(sys.argv) < 2:
    sys.stderr.write("Usage: %s infile.xml outfile.sb2\n" % sys.argv[0])
    sys.exit()

snap_project = xml.etree.ElementTree.parse(sys.argv[1])
snap_project_root = snap_project.getroot()
snap_project_sprites = None

if "app" in snap_project_root.attrib:
    print "Snap! project generated by \"%s\"" % snap_project_root.attrib["app"]
if "version" in snap_project_root.attrib:
    print "Snap! project version %s" % snap_project_root.attrib["version"]
print "\n"

scratch_project = kurt.Project()

for child in snap_project_root:
    if child.tag == "notes":
        # set project notes
        if child.text != None:
            scratch_project.notes = child.text
    if child.tag == "stage":
        print "Converting Stage..."

        # raise error if Stage has inheritance
        if child.attrib['inheritance'] == "true":
            raise notsupported.InheritanceNotSupportedError()

        stage_scripts = None
        # iterate over Stage element children
        for stage_child in child:
            if stage_child.tag == "sprites":
                snap_project_sprites = stage_child
            if stage_child.tag == "scripts":
                stage_scripts = stage_child

        # convert stage scripts
        print "> Converting scripts..."
        if stage_scripts == None:
            raise Exception("Stage scripts is None!")
        scratch_project.stage.scripts = scripts.convert_scripts(stage_scripts)


if snap_project_sprites == None:
    raise Exception("sprites is none!")

# convert all sprites
for sprite in snap_project_sprites.iter("sprite"):
    sprites.convert_sprite(sprite, scratch_project)

scratch_project.save(sys.argv[2])

print "\nDone!"
