# Copyright 2013,2014 Music Technology Group - Universitat Pompeu Fabra
# 
# This file is part of Dunya
# 
# Dunya is free software: you can redistribute it and/or modify it under the
# terms of the GNU Affero General Public License as published by the Free Software
# Foundation (FSF), either version 3 of the License, or (at your option) any later
# version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see http://www.gnu.org/licenses/

import conn
import json

def get_collections():
    """Get a list of all collections in the server."""
    path = "document/collections"
    return conn._get_paged_json(path)

def get_collection(slug):
    """Get the documents (recordings) in a collection.

    :param slug: the name of the collection

    """
    path = "document/%s" % slug
    return conn._dunya_query_json(path)

def document(recordingid):
    """Get the available source filetypes for a Musicbrainz recording.

    :param recordingid: Musicbrainz recording ID
    :returns: a list of filetypes in the database for this recording
      
    """
    path = "document/by-id/%s" % recordingid
    recording = conn._dunya_query_json(path)
    return recording

def file_for_document(recordingid, thetype, subtype=None, part=None, version=None):
    """Get the most recent derived file given a filetype.

    :param recordingid: Musicbrainz recording ID
    :param derivedtype: the computed filetype
    :param subtype: a subtype if the module has one
    :param part: the file part if the module has one
    :param version: a specific version, otherwise the most recent one will be used
    :returns: The contents of the most recent version of the derived file
      
    """
    path = "document/by-id/%s/%s" % (recordingid, thetype)
    args = {}
    if subtype:
        args["subtype"] = subtype
    if part:
        args["part"] = part
    if version:
        args["v"] = version
    return conn._dunya_query_file(path, **args)

def get_document_as_json(recordingid, thetype, subtype=None, part=None, version=None):
    """ Get a derived filetype and load it as json.

    :param recordingid: Musicbrainz recording ID
    :param derivedtype: the computed filetype
    :param subtype: a subtype if the module has one
    :param part: the file part if the module has one
    :param version: a specific version, otherwise the most recent one will be used

    """

    doc = file_for_document(recordingid, thetype, subtype, part, version)
    try:
        return json.loads(doc)
    except ValueError:
        return doc

