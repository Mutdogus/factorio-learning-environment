storage.actions.get_entities = function(player_index, radius, entity_names_json, position_x, position_y)
    local player = storage.agent_characters[player_index]
    local position
    if position_x and position_y then
        position = {x = tonumber(position_x), y = tonumber(position_y)}
    else
        position = player.position
    end

    radius = tonumber(radius) or 5
    local entity_names = entity_names_json and helpers.json_to_table(entity_names_json) or {}
    local area = {
        {position.x - radius, position.y - radius},
        {position.x + radius, position.y + radius}
    }

    local entities

    if #entity_names > 0 then
        entities = player.surface.find_entities_filtered{area = area, force = player.force, name = entity_names}
    else
        entities = player.surface.find_entities_filtered{area = area, force = player.force}
    end

    local result = {}
    for _, entity in ipairs(entities) do
        if entity.name ~= 'character' then
            local serialized = storage.utils.serialize_entity(entity)
            table.insert(result, serialized)
        end
    end
    return dump(result)
end
