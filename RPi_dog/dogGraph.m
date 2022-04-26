
file = input("Enter file name: ",'s');
A = readlines(file); %read lines into array
accel = zeros(length(A)-1,3);
gyro = zeros(length(A)-1,3);
time = zeros(length(A)-1,1);
line = split(A(2), ",")';
start = datetime(line(1),'InputFormat','yyyy-MM-dd HH:mm:ss.SSSSSS');

for i = 2:(length(A)-1)
    line = split(A(i), ",")';
    timestamp = datetime(line(1),'InputFormat','yyyy-MM-dd HH:mm:ss.SSSSSS');
    duration = timestamp-start;
    time(i-1) = seconds(duration);
    accel(i-1,:) = [line(2) line(3) line(4)];
    gyro(i-1,:) = [line(5) line(6) line(6)];
end

%time = time - time(1); %set time to start at 0
name = input("Enter plot title: ",'s');

subplot(2,1,1)

plot(time(1:end-1),accel(1:end-1, :))
legend("X", "Y", "Z")
xlabel("Time (seconds)")
ylabel("Acceleration (m/s^2")
title(name)
hold on
subplot(2,1,2)
plot(time(1:end-1),gyro(1:end-1, :))
legend("X", "Y", "Z")
xlabel("Time (seconds)")
ylabel("Angular Acceleration (degrees/s^2")


