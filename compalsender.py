#!/usr/bin/python -O
# Get the data from an UPC Connect Box
import asyncio
from pprint import pprint
import aiohttp
from connect_box import ConnectBox
from pyzabbix import ZabbixMetric, ZabbixSender

PASSWORD    = "pass"
IP          = "192.168.100.1"
HOST        = 'compal.lan'
ZBXSRV      = 'localhost'

async def main():
    async with aiohttp.ClientSession() as session:
        client = ConnectBox(session, PASSWORD, IP)

        # Get details about the downstream channel connectivity
        await client.async_get_downstream()

        # Get details about the upstream channel connectivity
        await client.async_get_upstream()

        # Get details on general device status
        await client.async_get_cmstatus_and_service_flows()

        # Get temperature status
        await client.async_get_temperature()

        # Close session
        await client.async_close_session()

        packet = [
          # Temperature
          ZabbixMetric(HOST, 'temperature[tuner]', client.temperature.tunerTemperature),
          ZabbixMetric(HOST, 'temperature[cpu]', client.temperature.temperature),
          # CmStatus
          ZabbixMetric(HOST, 'CmStatus.provisioningStatus', client.cmstatus.provisioningStatus),
          ZabbixMetric(HOST, 'CmStatus.cmComment', client.cmstatus.cmComment),
          ZabbixMetric(HOST, 'CmStatus.cmDocsisMode', client.cmstatus.cmDocsisMode),
          ZabbixMetric(HOST, 'CmStatus.cmNetworkAccess', client.cmstatus.cmNetworkAccess),
          ZabbixMetric(HOST, 'CmStatus.firmwareFilename', client.cmstatus.firmwareFilename),
          ZabbixMetric(HOST, 'CmStatus.numberOfCpes', client.cmstatus.numberOfCpes),
          ZabbixMetric(HOST, 'CmStatus.dMaxCpes', client.cmstatus.dMaxCpes),
          ZabbixMetric(HOST, 'CmStatus.bpiEnable', client.cmstatus.bpiEnable),
        ]
        # DownstreamChannel
        for channel in client.ds_channels :
             packet.extend([
                 ZabbixMetric(HOST, 'DownstreamChannel[' + str(channel.id) + '].frequency', channel.frequency),
                 ZabbixMetric(HOST, 'DownstreamChannel[' + str(channel.id) + '].powerLevel', channel.powerLevel),
                 ZabbixMetric(HOST, 'DownstreamChannel[' + str(channel.id) + '].modulation', channel.modulation),
                 ZabbixMetric(HOST, 'DownstreamChannel[' + str(channel.id) + '].snr', channel.snr),
                 ZabbixMetric(HOST, 'DownstreamChannel[' + str(channel.id) + '].preRs', channel.preRs),
                 ZabbixMetric(HOST, 'DownstreamChannel[' + str(channel.id) + '].postRs', channel.postRs),
                 ZabbixMetric(HOST, 'DownstreamChannel[' + str(channel.id) + '].qamLocked', channel.qamLocked),
                 ZabbixMetric(HOST, 'DownstreamChannel[' + str(channel.id) + '].fecLocked', channel.fecLocked),
                 ZabbixMetric(HOST, 'DownstreamChannel[' + str(channel.id) + '].mpegLocked', channel.mpegLocked)
             ])

        # UpstreamChannel
        for channel in client.us_channels :
            packet.extend([
                ZabbixMetric(HOST, 'UpstreamChannel[' + str(channel.id) + '].frequency', channel.frequency),
                ZabbixMetric(HOST, 'UpstreamChannel[' + str(channel.id) + '].powerLevel', channel.powerLevel),
                ZabbixMetric(HOST, 'UpstreamChannel[' + str(channel.id) + '].modulation', channel.modulation),
                ZabbixMetric(HOST, 'UpstreamChannel[' + str(channel.id) + '].symbolRate', channel.symbolRate),
                ZabbixMetric(HOST, 'UpstreamChannel[' + str(channel.id) + '].type', channel.type),
                ZabbixMetric(HOST, 'UpstreamChannel[' + str(channel.id) + '].t1Timeouts', channel.t1Timeouts),
                ZabbixMetric(HOST, 'UpstreamChannel[' + str(channel.id) + '].t2Timeouts', channel.t2Timeouts),
                ZabbixMetric(HOST, 'UpstreamChannel[' + str(channel.id) + '].t3Timeouts', channel.t3Timeouts),
                ZabbixMetric(HOST, 'UpstreamChannel[' + str(channel.id) + '].t4Timeouts', channel.t4Timeouts),
                ZabbixMetric(HOST, 'UpstreamChannel[' + str(channel.id) + '].channelType', channel.channelType),
                ZabbixMetric(HOST, 'UpstreamChannel[' + str(channel.id) + '].messageType', channel.messageType)
            ])

        # DownstreamChannel
        for dsf in client.downstream_service_flows :
             packet.extend([
                 ZabbixMetric(HOST, 'ServiceFlow[' + str(dsf.id) + '].pMaxTrafficRate', dsf.pMaxTrafficRate),
                 ZabbixMetric(HOST, 'ServiceFlow[' + str(dsf.id) + '].pMaxTrafficBurst', dsf.pMaxTrafficBurst),
                 ZabbixMetric(HOST, 'ServiceFlow[' + str(dsf.id) + '].pMinReservedRate', dsf.pMinReservedRate),
                 ZabbixMetric(HOST, 'ServiceFlow[' + str(dsf.id) + '].pMaxConcatBurst', dsf.pMaxConcatBurst),
                 ZabbixMetric(HOST, 'ServiceFlow[' + str(dsf.id) + '].pSchedulingType', dsf.pSchedulingType),
             ])

        for usf in client.upstream_service_flows :
             packet.extend([
                 ZabbixMetric(HOST, 'ServiceFlow[' + str(usf.id) + '].pMaxTrafficRate', usf.pMaxTrafficRate),
                 ZabbixMetric(HOST, 'ServiceFlow[' + str(usf.id) + '].pMaxTrafficBurst', usf.pMaxTrafficBurst),
                 ZabbixMetric(HOST, 'ServiceFlow[' + str(usf.id) + '].pMinReservedRate', usf.pMinReservedRate),
                 ZabbixMetric(HOST, 'ServiceFlow[' + str(usf.id) + '].pMaxConcatBurst', usf.pMaxConcatBurst),
                 ZabbixMetric(HOST, 'ServiceFlow[' + str(usf.id) + '].pSchedulingType', usf.pSchedulingType),
             ])
        result = ZabbixSender(ZBXSRV).send(packet)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
