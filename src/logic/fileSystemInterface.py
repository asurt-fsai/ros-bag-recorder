"""
Interface with the file system to read and write bags, list available bags, and delete bags.
"""

from typing import List, Dict, Any, Tuple

import os
import json
from ..constants import Constants


class FileSystemInterface:
    """
    Interface with the file system to read bags directory content, read json description file.
    """

    def __init__(self) -> None:
        self.bagDescription: Dict[str, Any] = {}

        if not os.path.exists(Constants.BAG_DIR_PATH):
            os.makedirs(Constants.BAG_DIR_PATH)

        self.loadDescriptionJson()

    def addBag(self, name: str, description: str) -> None:
        """
        Add bag to the json list

        Parameters
        ----------
        name: str
            name of the bag as ros saves it
        description: str
            description of the bag
        """
        parsedBagName = self._parsebagName(name)
        self.bagDescription[name] = {
            "description": description,
            "date": parsedBagName[1],
            "name": parsedBagName[0],
        }
        self.writeJsonToFile()

    def removeBag(self, name: str) -> None:
        """
        remove bag from the json list and deletes it from the file system if it exists

        Parameters
        ----------
        name: str
            name of the bag as ros saves it
        """

        self.bagDescription.pop(name)
        os.remove(os.path.join(Constants.BAG_DIR_PATH, name))
        self.writeJsonToFile()

    def writeJsonToFile(self) -> None:
        """
        writes self.description to the json file
        """
        j = json.dumps(self.bagDescription, indent=4)

        with open(
            os.path.join(Constants.BAG_DIR_PATH, Constants.JSON_FILE_NAME), "w", encoding="utf-8"
        ) as file:
            file.write(j)

    def loadDescriptionJson(self) -> None:
        """
        Load json file from the directory into self.bagDescription
        """

        bagsName = self._loadBagFileNames()

        try:
            with open(
                os.path.join(Constants.BAG_DIR_PATH, Constants.JSON_FILE_NAME),
                "r",
                encoding="utf-8",
            ) as file:
                self.bagDescription = json.loads(file.read())
        except IOError:
            with open(
                os.path.join(Constants.BAG_DIR_PATH, Constants.JSON_FILE_NAME),
                "w",
                encoding="utf-8",
            ) as file:
                self.bagDescription = {}
        except json.decoder.JSONDecodeError:
            self.bagDescription = {}

        self._syncFilesWithJson(bagsName)

    def _loadBagFileNames(self) -> List[str]:
        """
        Load the content of a directory.

        Returns
        -------
        List[str]
            List of file names in the directory.
        """

        fileNames = []

        for file in os.listdir(Constants.BAG_DIR_PATH):
            if file.endswith(".bag"):
                fileNames.append(file)

        return fileNames

    def _syncFilesWithJson(self, bagsName: List[str]) -> None:
        """
        Sync the content of the self.bagDescription with the given bagsName

        if bagName is not in self.bagDescription, add it with no description
        if self.bagDescription contain a name not in bagName. remove it.
        """

        for bagName in bagsName:
            if bagName not in self.bagDescription:
                parsedBagName = self._parsebagName(bagName)
                self.bagDescription[bagName] = {
                    "description": "",
                    "date": parsedBagName[1],
                    "name": parsedBagName[0],
                }

        for bagName in list(self.bagDescription.keys()):
            if bagName not in bagsName:
                self.bagDescription.pop(bagName)

        self.writeJsonToFile()

    def _parsebagName(self, bagName: str) -> Tuple[str, str]:
        """
        Given a bag name with the following format {prefix}_{timestamp}.bag

        it returns prefix and timestamp as date dd-mm-yyy

        Returns
        -------
        Tuple[str, str]
            Tuple of prefix name of the bag and the date in the format dd-mm-yyyy
        """

        parsedNameList = bagName.split(".")[0].split("_")
        name = parsedNameList[0]
        date = parsedNameList[1][:10]

        year = date[:4]
        month = date[5:7]
        day = date[8:10]

        return (name, f"{day}-{month}-{year}")
