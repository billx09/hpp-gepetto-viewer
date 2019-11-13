#!/usr/bin/env python

# Copyright (c) 2014 CNRS
# Author: Florent Lamiraux
#
# This file is part of hpp-gepetto-viewer.
# hpp-gepetto-viewer is free software: you can redistribute it
# and/or modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either version
# 3 of the License, or (at your option) any later version.
#
# hpp-gepetto-viewer is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Lesser Public License for more details.  You should have
# received a copy of the GNU Lesser General Public License along with
# hpp-gepetto-viewer.  If not, see
# <http://www.gnu.org/licenses/>.

import os
from hpp.gepetto import Viewer as Parent
from hpp.gepetto.viewer import _urdfPath, _srdfPath, _urdfSrdfFilenames

## Simultaneous control to hpp-manipulation-server and gepetto-viewer-server.
#
class Viewer (Parent):
    def __init__ (self, problemSolver, viewerClient = None, collisionURDF = False, *args, **kwargs) :
        self.compositeRobotName = problemSolver.robot.client.basic.robot.getRobotName()
        Parent.__init__ (self, problemSolver, viewerClient, collisionURDF, *args, **kwargs)

    def _initDisplay (self):
        if not self.client.gui.nodeExists(self.compositeRobotName):
            self.client.gui.createGroup (self.compositeRobotName)
            self.client.gui.addToGroup (self.compositeRobotName, self.sceneName)
        urdfFilename, srdfFilename = self.robot.urdfSrdfFilenames ()
        name = self.compositeRobotName + '/' + self.robot.robotNames[0]
        self.client.gui.addURDF (name, urdfFilename)
        if self.collisionURDF:
            self.toggleVisual(False)
        #self.client.gui.addToGroup (name, self.compositeRobotName)

    def loadRobotModel (self, RobotType, robotName, guiOnly = False, collisionURDF = False, frame = None):
        if not guiOnly:
            urdfFilename, srdfFilename = _urdfSrdfFilenames (RobotType)
            if frame is None:
                self.robot.insertRobotModel (robotName, RobotType.rootJointType,
                                             urdfFilename, srdfFilename)
            else:
                self.robot.insertRobotModelOnFrame (robotName, frame,
                                                    RobotType.rootJointType,
                                                    urdfFilename, srdfFilename)
        self.buildRobotBodies ()
        self.loadUrdfInGUI (RobotType, robotName)

    def loadHumanoidModel (self, RobotType, robotName, guiOnly = False):
        if not guiOnly:
            urdfFilename, srdfFilename = _urdfSrdfFilenames (RobotType)
            self.robot.loadHumanoidModel (robotName, RobotType.rootJointType,
                                          urdfFilename, srdfFilename)
        self.buildRobotBodies ()
        self.loadUrdfInGUI (RobotType, robotName)

    def loadEnvironmentModel (self, EnvType, envName, guiOnly = False):
        if not guiOnly:
            urdfFilename, srdfFilename = _urdfSrdfFilenames (EnvType)
            self.robot.loadEnvironmentModel (urdfFilename, srdfFilename,
                                             envName + "/")
        self.loadUrdfObjectsInGUI (EnvType, envName)
        self.computeObjectPosition ()

    def loadObjectModel (self, RobotType, robotName, guiOnly = False):
        if not guiOnly:
            urdfFilename, srdfFilename = _urdfSrdfFilenames (RobotType)
            self.robot.insertRobotModel (robotName, RobotType.rootJointType,
                                         urdfFilename, srdfFilename)
        self.buildRobotBodies ()
        base = "collision_" if self.collisionURDF else ""
        self.loadUrdfInGUI (RobotType, base + robotName)
        self.computeObjectPosition ()

    def buildCompositeRobot (self, robotNames):
        self.robot.buildCompositeRobot (robotNames)
        self.buildRobotBodies ()

    def loadUrdfInGUI (self, RobotType, robotName):
        # Load robot in viewer
        urdfFilename, srdfFilename = _urdfSrdfFilenames (RobotType)
        nodeName = self.compositeRobotName + "/" + robotName
        if self.collisionURDF:
            self.client.gui.addUrdfCollision (nodeName, urdfFilename)
        else:
            self.client.gui.addURDF (nodeName, urdfFilename)

    def loadUrdfObjectsInGUI (self, RobotType, robotName):
        urdfFilename, srdfFilename = _urdfSrdfFilenames (RobotType)
        self.client.gui.addUrdfObjects (robotName, urdfFilename,
                                        not self.collisionURDF)
        self.client.gui.addToGroup (robotName, self.sceneName)
