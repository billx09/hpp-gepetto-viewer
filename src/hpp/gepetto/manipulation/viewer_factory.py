#!/usr/bin/env python

# Copyright (c) 2015 CNRS
# Author: Florent Lamiraux, Joseph Mirabel
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
import warnings
from hpp.gepetto import ViewerFactory as Parent
from hpp.gepetto.manipulation import Viewer
from hpp.gepetto.viewer import _urdfPath, _srdfPath, _urdfSrdfFilenames

## Viewer factory for manipulation.Viewer
#
#  Store commands to be sent to \c gepetto-viewer-server, create
#  clients on demand and send stored commands.
class ViewerFactory (Parent):
    ## Constructor
    #  \param problemSolver instance of class
    #         manipulation.problem_solver.ProblemSolver
    def __init__ (self, problemSolver) :
        Parent.__init__ (self, problemSolver)

    def buildRobotBodies (self):
        l = locals ();
        self.guiRequest.append ((Viewer.buildRobotBodies, l));

    def loadRobotModel (self, RobotType, robotName, guiOnly = False, frame = None):
        l = locals ().copy ();
        if not guiOnly:
            urdfFilename, srdfFilename = _urdfSrdfFilenames (RobotType)
            if frame is None:
                self.robot.insertRobotModel (robotName, RobotType.rootJointType,
                                             urdfFilename, srdfFilename)
            else:
                self.robot.insertRobotModelOnFrame (robotName, frame,
                                                    RobotType.rootJointType,
                                                    urdfFilename, srdfFilename)
        l ['guiOnly'] = True
        self.guiRequest.append ((Viewer.loadRobotModel, l));

    def loadHumanoidModel (self, RobotType, robotName, guiOnly = False):
        l = locals ().copy ();
        if not guiOnly:
            urdfFilename, srdfFilename = _urdfSrdfFilenames (RobotType)
            self.robot.loadHumanoidModel (robotName, RobotType.rootJointType,
                                          urdfFilename, srdfFilename)
        l ['guiOnly'] = True
        self.guiRequest.append ((Viewer.loadHumanoidModel, l));

    def loadEnvironmentModel (self, EnvType, envName, guiOnly = False):
        l = locals ().copy ();
        if not guiOnly:
            urdfFilename, srdfFilename = _urdfSrdfFilenames (EnvType)
            self.robot.loadEnvironmentModel (urdfFilename, srdfFilename,
                                             envName + "/")
        l ['guiOnly'] = True
        self.guiRequest.append ((Viewer.loadEnvironmentModel, l));

    def loadObjectModel (self, RobotType, robotName, guiOnly = False):
        l = locals ().copy ()
        if not guiOnly:
            urdfFilename, srdfFilename = _urdfSrdfFilenames (RobotType)
            self.robot.insertRobotModel (robotName, RobotType.rootJointType,
                                         urdfFilename, srdfFilename)
        l ['guiOnly'] = True
        self.guiRequest.append ((Viewer.loadObjectModel, l));

    def buildCompositeRobot (self, robotNames):
        self.robot.buildCompositeRobot (robotNames)
        self.buildRobotBodies ()

    def loadUrdfInGUI (self, RobotType, robotName):
        self.guiRequest.append ((Viewer.loadUrdfInGUI, locals ()));

    def loadUrdfObjectsInGUI (self, RobotType, robotName):
        self.guiRequest.append ((Viewer.loadUrdfObjectsInGUI, locals ()));

    ## Create a client to \c gepetto-viewer-server and send stored commands
    #
    def createViewer (self, ViewerClass = Viewer, *args, **kwargs):
        return Parent.createViewer (self, ViewerClass, *args, **kwargs)
