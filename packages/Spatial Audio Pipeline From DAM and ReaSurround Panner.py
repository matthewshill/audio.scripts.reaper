import reaper_python as RPR

def createBusAndRouteTracks():
    track_count = RPR.CountSelectedTracks(0)
    
    # Create a 64 channel bus for the atmos objects
    RPR.InsertTrackAtIndex(0, False)
    atmos_bus = RPR.GetTrack(0, 0)
    RPR.SetMediaTrackInfo_Value(atmos_bus, "I_NCHAN", 64)
    RPR.GetSetMediaTrackInfo_String(atmos_bus, "P_NAME", "Atmos_Obj_Bus", True)
    
    for i in range(track_count):
        # Get selected MediaTrack
        source_track = RPR.GetSelectedTrack(0, i)
        prevFX_index = RPR.TrackFX_GetByName(source_track, "SpatialController", False)
        
        # Route selected track to atmos bus
        sendIndex = RPR.CreateTrackSend(source_track, atmos_bus)
        # REAPER needs i | 1024 to specify first mono output
        RPR.SetTrackSendInfo_Value(source_track, 0, sendIndex, "I_DSTCHAN", (i | 1024))
        RPR.SetTrackSendInfo_Value(source_track, 0, sendIndex, "I_SRCCHAN", (i | 1024))

def checkAndReplaceRSP():
    fx_name = "SpatialController"
    
    track_count = RPR.CountSelectedTracks(0)
    if track_count > 64:
        RPR.ShowConsoleMsg("WARNING: There is a limit of 64 tracks available. Please select less tracks.")
        return
    
    pluginExists = RPR.HasExtState("reaper_plugin_info", "com.msgv.SpatialController")
    if not pluginExists:
        RPR.ShowConsoleMsg("WARNING: Must add SpatialController Plugin to use this script.")
        return
    
    objId = 1
    for i in range(track_count):
        source_track = RPR.GetSelectedTrack(0, i)
        
        num_env = RPR.CountTrackEnvelopes(source_track)
        prevFX_index = RPR.TrackFX_GetByName(source_track, "ReaSurroundPan", False)
        x_envelope = RPR.GetTrackEnvelopeByName(source_track, "in 1 X / ReaSurroundPan")
        y_envelope = RPR.GetTrackEnvelopeByName(source_track, "in 1 Y / ReaSurroundPan")
        z_envelope = RPR.GetTrackEnvelopeByName(source_track, "in 1 Z / ReaSurroundPan")
        
        objIdIdx = 0
        posXIdx = 1
        posYIdx = 2
        posZIdx = 3
        
        if prevFX_index >= 0:
            newFX_index = RPR.TrackFX_AddByName(source_track, fx_name, False, -1)
            if x_envelope:
                _, automation_chunk = RPR.GetEnvelopeStateChunk(x_envelope, "", False)
                new_envelope = RPR.GetFXEnvelope(source_track, newFX_index, posXIdx, True)
                if new_envelope:
                    RPR.SetEnvelopeStateChunk(new_envelope, automation_chunk, False)
            
            if y_envelope:
                _, automation_chunk = RPR.GetEnvelopeStateChunk(y_envelope, "", False)
                new_envelope = RPR.GetFXEnvelope(source_track, newFX_index, posYIdx, True)
                if new_envelope:
                    RPR.SetEnvelopeStateChunk(new_envelope, automation_chunk, False)
            
            if z_envelope:
                _, automation_chunk = RPR.GetEnvelopeStateChunk(z_envelope, "", False)
                new_envelope = RPR.GetFXEnvelope(source_track, newFX_index, posZIdx, True)
                if new_envelope:
                    RPR.SetEnvelopeStateChunk(new_envelope, automation_chunk, False)
            
            x_val = RPR.TrackFX_GetParam(source_track, prevFX_index, 3)
            y_val = RPR.TrackFX_GetParam(source_track, prevFX_index, 4)
            z_val = RPR.TrackFX_GetParam(source_track, prevFX_index, 5)
            
            if x_val is not None:
                RPR.TrackFX_SetParam(source_track, newFX_index, 1, x_val)
            
            if y_val is not None:
                RPR.TrackFX_SetParam(source_track, newFX_index, 2, y_val)
            
            if z_val is not None:
                RPR.TrackFX_SetParam(source_track, newFX_index, 3, z_val)
            
            RPR.TrackFX_SetParam(source_track, newFX_index, objIdIdx, (objId / 128))
            objId += 1
            RPR.TrackFX_Delete(source_track, prevFX_index)

def checkAndReplaceDAM():
    fx_name = "SpatialController"
    
    track_count = RPR.CountSelectedTracks(0)
    if track_count > 64:
        RPR.ShowConsoleMsg("WARNING: There is a limit of 64 tracks available. Please select less tracks.")
        return
    
    pluginExists = RPR.HasExtState("reaper_plugin_info", "com.msgv.SpatialController")
    if not pluginExists:
        RPR.ShowConsoleMsg("WARNING: Must add SpatialController Plugin to use this script.")
        return
    
    objId = 1
    for i in range(track_count):
        source_track = RPR.GetSelectedTrack(0, i)
        
        num_env = RPR.CountTrackEnvelopes(source_track)
        prevFX_index = RPR.TrackFX_GetByName(source_track, "Dolby Atmos Music Panner", False)
        
        x_envelope = RPR.GetTrackEnvelopeByName(source_track, "Pan X / Dolby Atmos Music Panner")
        y_envelope = RPR.GetTrackEnvelopeByName(source_track, "Pan Y / Dolby Atmos Music Panner")
        z_envelope = RPR.GetTrackEnvelopeByName(source_track, "Pan Z / Dolby Atmos Music Panner")
        
        objIdIdx = 0
        posXIdx = 0
        posYIdx = 1
        posZIdx = 2
        
        if prevFX_index >= 0:
            newFX_index = RPR.TrackFX_AddByName(source_track, fx_name, False, -1)
            if x_envelope:
                _, automation_chunk = RPR.GetEnvelopeStateChunk(x_envelope, "", False)
                new_envelope = RPR.GetFXEnvelope(source_track, newFX_index, posXIdx, True)
                if new_envelope:
                    RPR.SetEnvelopeStateChunk(new_envelope, automation_chunk, False)
            
            if y_envelope:
                _, automation_chunk = RPR.GetEnvelopeStateChunk(y_envelope, "", False)
                new_envelope = RPR.GetFXEnvelope(source_track, newFX_index, posYIdx, True)
                if new_envelope:
                    RPR.SetEnvelopeStateChunk(new_envelope, automation_chunk, False)
            
            if z_envelope:
                _, automation_chunk = RPR.GetEnvelopeStateChunk(z_envelope, "", False)
                new_envelope = RPR.GetFXEnvelope(source_track, newFX_index, posZIdx, True)
                if new_envelope:
                    RPR.SetEnvelopeStateChunk(new_envelope, automation_chunk, False)
            
            x_val = RPR.TrackFX_GetParam(source_track, prevFX_index, 2)
            y_val = RPR.TrackFX_GetParam(source_track, prevFX_index, 3)
            z_val = RPR.TrackFX_GetParam(source_track, prevFX_index, 4)
            
            if x_val is not None:
                RPR.TrackFX_SetParam(source_track, newFX_index, 3, x_val)
            
            if y_val is not None:
                RPR.TrackFX_SetParam(source_track, newFX_index, 4, y_val)
            
            if z_val is not None:
                RPR.TrackFX_SetParam(source_track, newFX_index, 5, z_val)
            
            RPR.TrackFX_SetParam(source_track, newFX_index, objIdIdx, (objId / 128))
            objId += 1
            RPR.TrackFX_Delete(source_track, prevFX_index)

checkAndReplaceDAM()
checkAndReplaceRSP()
createBusAndRouteTracks()