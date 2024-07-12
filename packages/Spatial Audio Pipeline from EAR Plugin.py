#  ReaScript Name: Spatial Audio Pipeline From EAR Plugin
#  Author: Matthew S.Hill
#  Licence: GPL v3
#  REAPER: 5.0
#  Extensions: None
#  Version: 1.0
# 
#  Changelog:
#  v1.0 (2023)
#   Initial Release

import reaper_python as RPR

def setRenderLayer(atmos_bus, fx_name, layerIdx, renderLayerIdx):
    fxidx = RPR.TrackFX_GetByName(atmos_bus, fx_name, True)
    retval, value = RPR.TrackFX_GetParam(atmos_bus, fxidx, layerIdx)
    if retval and fxidx >= 0:
        RPR.TrackFX_SetParam(atmos_bus, fxidx, renderLayerIdx, value)

def main():
    fx_name = "PluginFXName"
    
    track_count = RPR.CountSelectedTracks(0)
    pluginExists = RPR.HasExtState("reaper_plugin_info", "com.acc.PluginName")
    
    if not pluginExists:
        RPR.ShowConsoleMsg("WARNING: Must add Plugin to use this script.")
        return
    
    if track_count > 64:
        RPR.ShowConsoleMsg("WARNING: There is a limit of 64 tracks available. Please select less tracks.")
        return
    
    objId = 1
    objIdIdx = 0
    posAIdx = 4
    posEIdx = 5
    posDIdx = 6
    layerIdx = 7
    renderLayerIdx = 9
    
    RPR.InsertTrackAtIndex(0, False)
    atmos_bus = RPR.GetTrack(0, 0)
    RPR.SetMediaTrackInfo_Value(atmos_bus, "I_NCHAN", 2)
    RPR.GetSetMediaTrackInfo_String(atmos_bus, "P_NAME", "Atmos_Obj_Bus", True)
    atmos_Fxidx = RPR.TrackFX_GetByName(atmos_bus, fx_name, True)
    
    for i in range(track_count):
        source_track = RPR.GetSelectedTrack(0, i)
        
        num_env = RPR.CountTrackEnvelopes(source_track)
        prevFX_index = RPR.TrackFX_GetByName(source_track, "EAR Object", False)
        
        a_envelope = RPR.GetTrackEnvelopeByName(source_track, "Azimuth / EAR Object")
        e_envelope = RPR.GetTrackEnvelopeByName(source_track, "Elevation / EAR Object")
        d_envelope = RPR.GetTrackEnvelopeByName(source_track, "Distance / EAR Object")
        
        if prevFX_index >= 0:
            newFX_index = RPR.TrackFX_GetByName(source_track, fx_name, True)
            
            if a_envelope:
                _, automation_chunk = RPR.GetEnvelopeStateChunk(a_envelope, "", False)
                new_envelope = RPR.GetFXEnvelope(source_track, newFX_index, posAIdx, True)
                if new_envelope:
                    RPR.SetEnvelopeStateChunk(new_envelope, automation_chunk, False)
            
            if e_envelope:
                _, automation_chunk = RPR.GetEnvelopeStateChunk(e_envelope, "", False)
                new_envelope = RPR.GetFXEnvelope(source_track, newFX_index, posEIdx, True)
                if new_envelope:
                    RPR.SetEnvelopeStateChunk(new_envelope, automation_chunk, False)
            
            if d_envelope:
                _, automation_chunk = RPR.GetEnvelopeStateChunk(d_envelope, "", False)
                new_envelope = RPR.GetFXEnvelope(source_track, newFX_index, posDIdx, True)
                if new_envelope:
                    RPR.SetEnvelopeStateChunk(new_envelope, automation_chunk, False)
            
            azimuth_val = RPR.TrackFX_GetParam(source_track, prevFX_index, 3)
            distance_val = RPR.TrackFX_GetParam(source_track, prevFX_index, 4)
            elevation_val = (RPR.TrackFX_GetParam(source_track, prevFX_index, 5) + 90) / 180
            
            if azimuth_val is not None:
                RPR.TrackFX_SetParam(source_track, newFX_index, posAIdx, azimuth_val)
            
            if elevation_val is not None:
                RPR.TrackFX_SetParam(source_track, newFX_index, posEIdx, elevation_val)
            
            if distance_val is not None:
                RPR.TrackFX_SetParam(source_track, newFX_index, posDIdx, distance_val)
            
            RPR.TrackFX_SetParam(source_track, newFX_index, objIdIdx, objId / 128)
            objId += 1
            
            RPR.TrackFX_Delete(source_track, prevFX_index)
            RPR.SetMediaTrackInfo_Value(source_track, "I_NCHAN", 64)
            sendIndex = RPR.CreateTrackSend(source_track, atmos_bus)
            RPR.SetTrackSendInfo_Value(source_track, 0, sendIndex, "I_DSTCHAN", i | 1024)
            RPR.SetTrackSendInfo_Value(source_track, 0, sendIndex, "I_SRCCHAN", i | 1024)
    
    RPR.defer(lambda: setRenderLayer(atmos_bus, fx_name, layerIdx, renderLayerIdx))
    RPR.UpdateArrange()

main()