package cn.edu.tsinghua.thss.popcorn;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.lidroid.xutils.HttpUtils;
import com.lidroid.xutils.ViewUtils;
import com.lidroid.xutils.exception.HttpException;
import com.lidroid.xutils.http.RequestParams;
import com.lidroid.xutils.http.ResponseInfo;
import com.lidroid.xutils.http.callback.RequestCallBack;
import com.lidroid.xutils.http.client.HttpRequest;
import com.lidroid.xutils.view.annotation.ViewInject;
import com.lidroid.xutils.view.annotation.event.OnClick;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;

import cn.edu.tsinghua.thss.popcorn.config.Config;
import cn.edu.tsinghua.thss.popcorn.ui.MineFragment;
import cn.edu.tsinghua.thss.popcorn.utils.NoRepeatToast;


public class UserInfoActivity extends Activity {
    private String name;
    private String department;
    private String gender;
    private String mobile;
    private String email;
    private String address;
    private String birthday;
    private String[] items = new String[] { "选择本地图片", "拍照" };
    private static final int IMAGE_REQUEST_CODE = 0;
    private static final int CAMERA_REQUEST_CODE = 1;
    private static final int RESULT_REQUEST_CODE = 2;
    private static final String IMAGE_FILE_NAME = Config.DEBUG_USERNAME+".jpg";

    @ViewInject(R.id.user_info_avatar)
    private ImageView userInfoAvatar;

    @ViewInject(R.id.user_info_name)
    private TextView userInfoName;

    @ViewInject(R.id.user_info_department)
    private TextView userInfoDepartment;

    @ViewInject(R.id.user_info_gender)
    private TextView userInfoGender;

    @ViewInject(R.id.user_info_mobile)
    private TextView userInfoMobile;

    @ViewInject(R.id.user_info_email)
    private TextView userInfoEmail;

    @ViewInject(R.id.user_info_address)
    private TextView userInfoAddress;

    @ViewInject(R.id.user_info_birthday)
    private TextView userInfoBirthday;


    public static boolean hasSdcard(){
        String state = Environment.getExternalStorageState();
        if(state.equals(Environment.MEDIA_MOUNTED)){
            return true;
        }else{
            return false;
        }
    }

    @OnClick(R.id.user_info_avatar_ll)
    private void onUserInfoAvatarClick(View v){
        new AlertDialog.Builder(this)
                .setTitle("设置头像")
                .setItems(items, new DialogInterface.OnClickListener() {

                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        switch (which) {
                            case 0:
                                Intent intentFromGallery = new Intent();
                                intentFromGallery.setType("image/*"); // 设置文件类型
                                intentFromGallery
                                        .setAction(Intent.ACTION_GET_CONTENT);
                                startActivityForResult(intentFromGallery,
                                        IMAGE_REQUEST_CODE);
                                break;
                            case 1:
                                Intent intentFromCapture = new Intent(
                                        MediaStore.ACTION_IMAGE_CAPTURE);
                                // 判断存储卡是否可以用，可用进行存储
                                if (hasSdcard()) {
                                    String file_path = Config.AVATAR_FILE_DIR;
                                    File path = new File(file_path);
                                    File file = new File(path,IMAGE_FILE_NAME);

                                    intentFromCapture.putExtra(
                                            MediaStore.EXTRA_OUTPUT,
                                            Uri.fromFile(file));
                                }

                                startActivityForResult(intentFromCapture,CAMERA_REQUEST_CODE);
                                break;
                        }
                    }
                })
                .setNegativeButton("取消", new DialogInterface.OnClickListener() {

                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                    }
                }).show();
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        //结果码不等于取消时候
        if (resultCode != RESULT_CANCELED) {

            switch (requestCode) {
                case IMAGE_REQUEST_CODE:
                    startPhotoZoom(data.getData());
                    break;
                case CAMERA_REQUEST_CODE:
                    if (hasSdcard()) {
                       //File path = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DCIM);
                        String file_path = Environment.getExternalStorageDirectory().getPath() + "/willwings/avatar/";
                        File path = new File(file_path);
                        if (!path.exists()) {
                            path.mkdirs();
                        }
                        File tempFile = new File(path,IMAGE_FILE_NAME);
                        startPhotoZoom(Uri.fromFile(tempFile));
                    } else {
                        Toast.makeText(this, "未找到存储卡，无法存储照片！",Toast.LENGTH_LONG).show();
                    }
                    break;
                case RESULT_REQUEST_CODE: //图片缩放完成后
                    if (data != null) {
                        getImageToView(data);
                    }
                    break;
            }
        }
        super.onActivityResult(requestCode, resultCode, data);
    }

    /**
     * 裁剪图片方法实现
     *
     * @param uri
     */
    public void startPhotoZoom(Uri uri) {
        Intent intent = new Intent("com.android.camera.action.CROP");
        intent.setDataAndType(uri, "image/*");
        // 设置裁剪
        intent.putExtra("crop", "true");
        // aspectX aspectY 是宽高的比例
        intent.putExtra("aspectX", 1);
        intent.putExtra("aspectY", 1);
        // outputX outputY 是裁剪图片宽高
        intent.putExtra("outputX", 340);
        intent.putExtra("outputY", 340);
        intent.putExtra("return-data", true);
        startActivityForResult(intent, RESULT_REQUEST_CODE);
    }

    /**
     * 保存裁剪之后的图片数据
     * @param data
     */
    private void getImageToView(Intent data) {
        Bundle extras = data.getExtras();
        if (extras != null) {
            Bitmap photo = extras.getParcelable("data");
           // Drawable drawable = new BitmapDrawable(this.getResources(),photo);
            userInfoAvatar.setImageBitmap(photo);
            saveBitmap(photo, Config.AVATAR_FILE_DIR+IMAGE_FILE_NAME);

            RequestParams params = new RequestParams();
            params.addBodyParameter("username", Config.DEBUG_USERNAME);
            params.addBodyParameter("access_token", Config.ACCESS_TOKEN);
            params.addBodyParameter("avatar", new File(Config.AVATAR_FILE_DIR+IMAGE_FILE_NAME));

            HttpUtils http = new HttpUtils();
            http.send(HttpRequest.HttpMethod.POST,
                    Config.SUBMIT_AVATAR_URL,
                    params,
                    new RequestCallBack<String>() {

                        @Override
                        public void onStart() {
                        }

                        @Override
                        public void onLoading(long total, long current, boolean isUploading) {

                        }

                        @Override
                        public void onSuccess(ResponseInfo<String> responseInfo) {
                        }

                        @Override
                        public void onFailure(HttpException error, String msg) {
                        }
                    }
            );
        }
    }

    private void saveBitmap(Bitmap bm, String path) {
        File f = new File(path);
//        if (f.exists()) {
//            f.delete();
//        }
        try {
            FileOutputStream out = new FileOutputStream(f);
            bm.compress(Bitmap.CompressFormat.JPEG, 90, out);
            out.flush();
            out.close();
        } catch (FileNotFoundException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

    }

    @OnClick(R.id.user_info_name_ll)
    private void onUserInfoNameClick(View v){
        final EditText mEditText = new EditText(this);
        mEditText.setText(userInfoName.getText());
        mEditText.setSelection(userInfoName.getText().length());
        new AlertDialog.Builder(this).setTitle("修改姓名").setView(
                mEditText
        ).setPositiveButton("确定", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog,
                                int which) {
                // TODO Auto-generated method stub
                RequestParams params = new RequestParams();
                params.addBodyParameter("username", Config.DEBUG_USERNAME);
                params.addBodyParameter("access_token", Config.ACCESS_TOKEN);
                params.addBodyParameter("name", mEditText.getText().toString());

                HttpUtils http = new HttpUtils();
                http.send(HttpRequest.HttpMethod.POST,
                        Config.SUBMIT_USER_INFO_URL,
                        params,
                        new RequestCallBack<String>() {

                            @Override
                            public void onStart() {
                            }

                            @Override
                            public void onLoading(long total, long current, boolean isUploading) {

                            }

                            @Override
                            public void onSuccess(ResponseInfo<String> responseInfo) {
                                userInfoName.setText(mEditText.getText());
                            }

                            @Override
                            public void onFailure(HttpException error, String msg) {
                            }
                        });
            }
    }).setNegativeButton("取消", null).show();
    }

    private int selectedIndex = 0;
    private String mGender = "";
    @OnClick(R.id.user_info_gender_ll)
    private void onUserInfoGenderClick(View v){
        if(userInfoGender.getText() == "男"){
            selectedIndex = 0;
        }else{
            selectedIndex = 1;
        }
        new AlertDialog.Builder(this).setTitle("修改性别").setSingleChoiceItems(
                new String[]{"男", "女"}, selectedIndex, new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        selectedIndex = which;
                    }
                }
        ).setPositiveButton("确定", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog,
                                int which) {
                // TODO Auto-generated method stub
                if (selectedIndex == 1){
                    mGender = "女";
                }else{
                    mGender = "男";
                }
                RequestParams params = new RequestParams();
                params.addBodyParameter("username", Config.DEBUG_USERNAME);
                params.addBodyParameter("access_token", Config.ACCESS_TOKEN);
                if(mGender.equals("男")){
                    params.addBodyParameter("gender", "1");
                }else{
                    params.addBodyParameter("gender", "0");
                }

                HttpUtils http = new HttpUtils();
                http.send(HttpRequest.HttpMethod.POST,
                        Config.SUBMIT_USER_INFO_URL,
                        params,
                        new RequestCallBack<String>() {

                            @Override
                            public void onStart() {
                            }

                            @Override
                            public void onLoading(long total, long current, boolean isUploading) {

                            }

                            @Override
                            public void onSuccess(ResponseInfo<String> responseInfo) {
                                userInfoGender.setText(mGender);
                            }

                            @Override
                            public void onFailure(HttpException error, String msg) {
                            }
                        });
            }
        }).setNegativeButton("取消", null).show();
    }

    @OnClick(R.id.user_info_birthday_ll)
    private void onUserInfoBirthdayClick(View v){
        final EditText mEditText = new EditText(this);
        mEditText.setText(userInfoBirthday.getText());
        mEditText.setSelection(userInfoBirthday.getText().length());
        new AlertDialog.Builder(this).setTitle("修改生日").setView(
                mEditText
        ).setPositiveButton("确定", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog,
                                int which) {
                // TODO Auto-generated method stub
                RequestParams params = new RequestParams();
                params.addBodyParameter("username", Config.DEBUG_USERNAME);
                params.addBodyParameter("access_token", Config.ACCESS_TOKEN);
                params.addBodyParameter("birthday", mEditText.getText().toString());

                HttpUtils http = new HttpUtils();
                http.send(HttpRequest.HttpMethod.POST,
                        Config.SUBMIT_USER_INFO_URL,
                        params,
                        new RequestCallBack<String>() {

                            @Override
                            public void onStart() {
                            }

                            @Override
                            public void onLoading(long total, long current, boolean isUploading) {

                            }

                            @Override
                            public void onSuccess(ResponseInfo<String> responseInfo) {
                                userInfoBirthday.setText(mEditText.getText());
                            }

                            @Override
                            public void onFailure(HttpException error, String msg) {
                            }
                        });
            }
        }).setNegativeButton("取消", null).show();
    }

    @OnClick(R.id.user_info_mobile_ll)
    private void onUserInfoMobileClick(View v){
        final EditText mEditText = new EditText(this);
        mEditText.setText(userInfoMobile.getText());
        mEditText.setSelection(userInfoMobile.getText().length());
        new AlertDialog.Builder(this).setTitle("修改手机号").setView(
                mEditText
        ).setPositiveButton("确定", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog,
                                int which) {
                // TODO Auto-generated method stub
                RequestParams params = new RequestParams();
                params.addBodyParameter("username", Config.DEBUG_USERNAME);
                params.addBodyParameter("access_token", Config.ACCESS_TOKEN);
                params.addBodyParameter("mobile", mEditText.getText().toString());

                HttpUtils http = new HttpUtils();
                http.send(HttpRequest.HttpMethod.POST,
                        Config.SUBMIT_USER_INFO_URL,
                        params,
                        new RequestCallBack<String>() {

                            @Override
                            public void onStart() {
                            }

                            @Override
                            public void onLoading(long total, long current, boolean isUploading) {

                            }

                            @Override
                            public void onSuccess(ResponseInfo<String> responseInfo) {
                                userInfoMobile.setText(mEditText.getText());
                            }

                            @Override
                            public void onFailure(HttpException error, String msg) {
                            }
                        });
            }
        }).setNegativeButton("取消", null).show();
    }

    @OnClick(R.id.user_info_email_ll)
    private void onUserInfoEmailClick(View v){
        final EditText mEditText = new EditText(this);
        mEditText.setText(userInfoEmail.getText());
        mEditText.setSelection(userInfoEmail.getText().length());
        new AlertDialog.Builder(this).setTitle("修改邮箱").setView(
                mEditText
        ).setPositiveButton("确定", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog,
                                int which) {
                // TODO Auto-generated method stub
                RequestParams params = new RequestParams();
                params.addBodyParameter("username", Config.DEBUG_USERNAME);
                params.addBodyParameter("access_token", Config.ACCESS_TOKEN);
                params.addBodyParameter("email", mEditText.getText().toString());

                HttpUtils http = new HttpUtils();
                http.send(HttpRequest.HttpMethod.POST,
                        Config.SUBMIT_USER_INFO_URL,
                        params,
                        new RequestCallBack<String>() {

                            @Override
                            public void onStart() {
                            }

                            @Override
                            public void onLoading(long total, long current, boolean isUploading) {

                            }

                            @Override
                            public void onSuccess(ResponseInfo<String> responseInfo) {
                                userInfoEmail.setText(mEditText.getText());
                            }

                            @Override
                            public void onFailure(HttpException error, String msg) {
                            }
                        });
            }
        }).setNegativeButton("取消", null).show();
    }

    @OnClick(R.id.user_info_address_ll)
    private void onUserInfoAddressClick(View v){
        final EditText mEditText = new EditText(this);
        mEditText.setText(userInfoAddress.getText());
        mEditText.setSelection(userInfoAddress.getText().length());
        new AlertDialog.Builder(this).setTitle("修改住址").setView(
                mEditText
        ).setPositiveButton("确定", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog,
                                int which) {
                // TODO Auto-generated method stub
                RequestParams params = new RequestParams();
                params.addBodyParameter("username", Config.DEBUG_USERNAME);
                params.addBodyParameter("access_token", Config.ACCESS_TOKEN);
                params.addBodyParameter("address", mEditText.getText().toString());

                HttpUtils http = new HttpUtils();
                http.send(HttpRequest.HttpMethod.POST,
                        Config.SUBMIT_USER_INFO_URL,
                        params,
                        new RequestCallBack<String>() {

                            @Override
                            public void onStart() {
                            }

                            @Override
                            public void onLoading(long total, long current, boolean isUploading) {

                            }

                            @Override
                            public void onSuccess(ResponseInfo<String> responseInfo) {
                                userInfoAddress.setText(mEditText.getText());
                            }

                            @Override
                            public void onFailure(HttpException error, String msg) {
                            }
                        }
                );
            }
        }).setNegativeButton("取消", null).show();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_user_info);
        ViewUtils.inject(this);
    }

    private Bitmap getDiskBitmap(String pathString)
    {
        Bitmap bitmap = null;
        try
        {
            File file = new File(pathString);
            if(file.exists())
            {
                bitmap = BitmapFactory.decodeFile(pathString);
            }
        } catch (Exception e)
        {
            // TODO: handle exception
        }
        return bitmap;
    }

    @Override
    public void onStart(){
        super.onStart();
        getUserInfo();
    }

    private void getUserInfo(){
        Bitmap photo = getDiskBitmap(Config.AVATAR_FILE_DIR+IMAGE_FILE_NAME);
        if(photo!=null){
            //Drawable drawable = new BitmapDrawable(this.getResources(),photo);
            userInfoAvatar.setImageBitmap(photo);
        }

        RequestParams params = new RequestParams();
        params.addQueryStringParameter("username", Config.DEBUG_USERNAME);
        params.addQueryStringParameter("access_token", Config.ACCESS_TOKEN);

        HttpUtils http = new HttpUtils();
        http.configCurrentHttpCacheExpiry(Config.MAX_NETWORK_TIME);
        http.send(HttpRequest.HttpMethod.GET,
                Config.GET_USER_INFO_URL,
                params,
                new RequestCallBack<String>() {

                    @Override
                    public void onStart() {
                    }

                    @Override
                    public void onLoading(long total, long current, boolean isUploading) {
                    }

                    @Override
                    public void onSuccess(ResponseInfo<String> responseInfo) {
                        try {
                            JSONObject jsonObject = new JSONObject(responseInfo.result);
                            String status = jsonObject.getString("status");


                            if (status.equals("ok")) {
                                JSONObject userInfo = jsonObject.getJSONObject("data");
                                name = userInfo.getString("name");
                                gender = userInfo.getString("gender");
                                if(gender.equals("1")){
                                    gender="男";
                                }else{
                                    gender="女";
                                }
                                birthday = userInfo.getString("birthday");
                                mobile = userInfo.getString("mobile");
                                email = userInfo.getString("email");
                                department = userInfo.getString("department");
                                address = userInfo.getString("address");
                                setUserInfoView();
                            } else {
                                Toast.makeText(getApplicationContext(), "网络连接出错", Toast.LENGTH_SHORT).show();
                            }

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }


                    @Override
                    public void onFailure(HttpException error, String msg) {
                        //Toast.makeText(getApplicationContext(), "网络连接异常，请检查网络连接！", Toast.LENGTH_SHORT).show();
                        NoRepeatToast.showToast(getApplicationContext(), "网络连接异常，请检查网络连接！", Toast.LENGTH_SHORT);
                    }
                });
    }

    private  void setUserInfoView(){
        userInfoName.setText(name);
        userInfoGender.setText(gender);
        userInfoBirthday.setText(birthday);
        userInfoMobile.setText(mobile);
        userInfoEmail.setText(email);
        userInfoDepartment.setText(department);
        userInfoAddress.setText(address);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_user_info, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.close_btn) {
            this.finish();
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}
